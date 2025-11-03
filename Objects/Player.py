from GameFrame import RoomObject, Globals
import pygame
import sys
from random import choice
from Objects.Hud import Text   # HUD text
from Objects.NPC import NPC  # NPC class

class Player(RoomObject):
    """
    A class for the player's avatar (the Ship)
    """

    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        image = self.load_image("Player_right.png")
        self.set_image(image, 200, 200)
        self.interacted = False
        self.handle_key_events = True
        self.register_collision_object("NPC")

        # Collision tracking
        self._in_npc_collision = False  # flag to avoid re-drawing text every frame

    # ------------------------------------------------------------
    # Utility: force reload of background from disk
    # ------------------------------------------------------------
    def _force_set_background(self, image_name):
        """Force reload the background image even if cached."""
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        gameframe_dir = os.path.join(base_dir, "..")
        images_dir = os.path.join(gameframe_dir, "images")
        full_path = os.path.join(images_dir, image_name)
        full_path = os.path.normpath(full_path)

        self.room.background_image = pygame.image.load(full_path).convert()
        self.room.set_background_image(image_name)

    # ------------------------------------------------------------
    # Utility: swap sprite image but keep rect size/position
    # ------------------------------------------------------------
    def _set_player_image(self, filename):
        image = self.load_image(filename)
        old_center = self.rect.center if hasattr(self, "rect") else (self.x, self.y)
        self.set_image(image, 200, 200)
        self.rect.center = old_center

        # shrink collision box if needed
        hitbox_width, hitbox_height = 80, 80
        self.rect.width = hitbox_width
        self.rect.height = hitbox_height
        self.rect.center = old_center
        

    # ------------------------------------------------------------
    # Handle key inputs and collisions
    # ------------------------------------------------------------
    def key_pressed(self, key):
        distance = 30
        moved = False
        if key[pygame.K_LSHIFT]:
            distance = 60

        if key[pygame.K_w]:
            self._set_player_image("Player_looking_backwards.png")
            self.y -= distance
            moved = True
        elif key[pygame.K_s]:
            self._set_player_image("Player_looking_forwards.png")
            self.y += distance
            moved = True
        elif key[pygame.K_a]:
            self._set_player_image("Player_left.png")
            self.x -= distance
            moved = True
        elif key[pygame.K_d]:
            self._set_player_image("Player_right.png")
            self.x += distance
            moved = True
        elif key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        else:
            self._set_player_image("Player_looking_forwards.png")

        self.Keep_In_Room()

        if moved:
            self._handle_background_change()

        # Award score if Y is pressed while colliding with an NPC
        if key[pygame.K_y] and self._in_npc_collision:
            for obj in self.room.objects:
                if obj.__class__.__name__ == "NPC" and self.rect.colliderect(obj.rect):
                    if not getattr(obj, "interacted", False):
                        obj.interacted = True
                        if hasattr(obj, "score_value") and hasattr(self.room, "score"):
                            self.room.score.update_score(obj.score_value)
        elif key[pygame.K_n] and self._in_npc_collision:
            for obj in self.room.objects:
                if obj.__class__.__name__ == "NPC" and self.rect.colliderect(obj.rect):
                    if not getattr(obj, "interacted", False):
                        obj.interacted = True
                        if hasattr(self.room, "friend_text"):
                            self.room.friend_text.text = "Maybe next time!"
                            self.room.friend_text.render_text()
                            if hasattr(obj, "worthyness") and hasattr(self.room, "score"):
                                self.room.score.update_score(obj.worthyness)
                            

        self._handle_room_transitions()
        print(f"Player position: ({self.x}, {self.y})")

    # ------------------------------------------------------------
    # Check collisions with NPCs and update background + text
    # ------------------------------------------------------------
    def _handle_background_change(self):
        colliding = False

        for obj in self.room.objects:
            if obj.__class__.__name__ == "NPC":
                if self.rect.colliderect(obj.rect):
                    colliding = True
                    break

        if colliding and not self._in_npc_collision:
            # entering collision
            self._in_npc_collision = True

            if type(self.room).__name__ == "Path":
                self._force_set_background("Text_Path.png")
            elif type(self.room).__name__ == "School_Pathway":
                self._force_set_background("School_Path_text.png")

            if hasattr(self.room, "friend_text"):
                self.room.friend_text.update_text()

        elif not colliding and self._in_npc_collision:
            # exiting collision
            self._in_npc_collision = False

            if type(self.room).__name__ == "Path":
                self._force_set_background("Path.png")
            elif type(self.room).__name__ == "School_Pathway":
                self._force_set_background("School_Path.png")

            if hasattr(self.room, "friend_text"):
                self.room.friend_text.text = ""
                self.room.friend_text.render_text()

    # ------------------------------------------------------------
    # Keep player inside the visible room
    # ------------------------------------------------------------
    def Keep_In_Room(self):
        if self.x < 190:
            self.x = 190
        if self.y < 100:
            self.y = 100
        if self.x > 1610:
            self.x = 1610
        if self.y > 800:
            self.y = 800

    # ------------------------------------------------------------
    # Handle transitions between rooms
    # ------------------------------------------------------------
    def _handle_room_transitions(self):
        if self.x >= 1500 and hasattr(self.room, "request_room_change") and type(self.room).__name__ == "Path":
            prev_index = Globals.level_history[-1]
            Globals.next_level = prev_index + 1
            self.room.done = True

        if self.x <= 200 and hasattr(self.room, "request_room_change") and type(self.room).__name__ == "School_Pathway":
            if len(Globals.level_history) >= 2:
                prev_index = Globals.level_history[-2]
                Globals.next_level = prev_index
                self.room.done = True
            else:
                if "Path" in Globals.levels:
                    Globals.next_level = Globals.levels.index("Path")
                    self.room.done = True

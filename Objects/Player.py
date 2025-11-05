from GameFrame import RoomObject, Globals
import pygame
import os
from Objects.NPC import NPC  # NPC class


class Player(RoomObject):
    """
    A class for the player's avatar
    """

    def __init__(self, room, x, y):
        super().__init__(room, x, y)

        # initial sprite
        image = self.load_image("Player_right.png")
        self.set_image(image, 200, 200)

        self.interacted = False
        self.handle_key_events = True
        self.register_collision_object("NPC")

        # persist available_friends across rooms
        if not hasattr(Globals, "available_friends"):
            Globals.available_friends = 5
        self.available_friends = Globals.available_friends

        # collision tracking
        self._in_npc_collision = False

    # ------------------------------------------------------------
    # Utility: force reload of background from disk
    # ------------------------------------------------------------
    def _force_set_background(self, image_name):
        """Force reload the background image even if cached."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        gameframe_dir = os.path.join(base_dir, "..")
        images_dir = os.path.join(gameframe_dir, "images")
        full_path = os.path.normpath(os.path.join(images_dir, image_name))

        self.room.background_image = pygame.image.load(full_path).convert()
        self.room.set_background_image(image_name)

    # ------------------------------------------------------------
    # Utility: swap sprite image but keep rect size/position
    # ------------------------------------------------------------
    def _set_player_image(self, filename):
        image = self.load_image(filename)
        old_center = self.rect.center if hasattr(self, "rect") else (self.x, self.y)
        self.set_image(image, 200, 200)

        # shrink collision box if needed
        self.rect.width, self.rect.height = 150, 150
        self.rect.center = old_center

    # ------------------------------------------------------------
    # Helper: get colliding NPC (if any)
    # ------------------------------------------------------------
    def _get_colliding_npc(self):
        for obj in self.room.objects:
            if isinstance(obj, NPC) and self.rect.colliderect(obj.rect):
                return obj
        return None

    # ------------------------------------------------------------
    # Handle key inputs and collisions
    # ------------------------------------------------------------
    def key_pressed(self, key):
        distance = 60 if key[pygame.K_LSHIFT] else 30
        moved = False

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
            Globals.next_level = Globals.levels.index("WelcomeScreen")
            self.room.done = True
        elif key[pygame.K_e]:
            Globals.next_level = Globals.levels.index("Phone")
            self.room.done = True
        else:
            self._set_player_image("Player_looking_forwards.png")

        self.Keep_In_Room()

        if moved:
            self._handle_background_change()

        # Friend interaction
        npc = self._get_colliding_npc()
        if npc and key[pygame.K_y] and not getattr(npc, "interacted", False):
            npc.interacted = True
            if hasattr(npc, "score_value") and hasattr(self.room, "score") and self.available_friends > 0:
                self.room.score.update_score(npc.score_value)
                self.available_friends -= 1
                Globals.available_friends = self.available_friends
                print(self.available_friends)
            elif self.available_friends <= 0 and hasattr(self.room, "friend_text"):
                self.room.friend_text.text = "You've already made 5 friends! I guess I can't friend you..."
                self.room.friend_text.render_text()

        elif npc and key[pygame.K_n] and not getattr(npc, "interacted", False):
            npc.interacted = True
            if hasattr(self.room, "friend_text"):
                self.room.friend_text.text = "Maybe next time!"
                self.room.friend_text.render_text()
                if hasattr(npc, "worthyness") and hasattr(self.room, "score"):
                    self.room.score.update_score(npc.worthyness)

        self._handle_room_transitions()

    # ------------------------------------------------------------
    # Check collisions with NPCs and update background + text
    # ------------------------------------------------------------
    def _handle_background_change(self):
        npc = self._get_colliding_npc()
        colliding = npc is not None

        if colliding and not self._in_npc_collision:
            self._in_npc_collision = True
            bg_map = {
                "Path": "Text_Path.png",
                "School_Pathway": "School_Path_text.png"
            }
            self._force_set_background(bg_map.get(type(self.room).__name__, ""))

            if hasattr(self.room, "friend_text"):
                self.room.friend_text.update_text()

        elif not colliding and self._in_npc_collision:
            self._in_npc_collision = False
            bg_map = {
                "Path": "Path.png",
                "School_Pathway": "School_Path.png"
            }
            self._force_set_background(bg_map.get(type(self.room).__name__, ""))

            if hasattr(self.room, "friend_text"):
                self.room.friend_text.text = ""
                self.room.friend_text.render_text()

    # ------------------------------------------------------------
    # Keep player inside the visible room
    # ------------------------------------------------------------
    def Keep_In_Room(self):
        # Use screen size dynamically instead of hard-coded values
        w, h = self.room.screen.get_width(), self.room.screen.get_height()
        self.x = max(0, min(self.x, w - self.rect.width))
        self.y = max(0, min(self.y, h - self.rect.height))

    # ------------------------------------------------------------
    # Handle transitions between rooms
    # ------------------------------------------------------------
    def _handle_room_transitions(self):
        room_name = type(self.room).__name__

        if room_name == "Path" and self.x >= 1500 and hasattr(self.room, "request_room_change"):
            prev_index = Globals.level_history[-1]
            Globals.next_level = prev_index + 1
            self.room.done = True

        elif room_name == "School_Pathway" and self.x <= 200 and hasattr(self.room, "request_room_change"):
            if len(Globals.level_history) >= 2:
                prev_index = Globals.level_history[-2]
                Globals.next_level = prev_index
            elif "Path" in Globals.levels:
                Globals.next_level = Globals.levels.index("Path")
            self.room.done = True

from GameFrame import RoomObject, Globals
import pygame
import os
from Objects.NPC import NPC

class Player(RoomObject):
    """
    Controls the player's avatar - movement, sprite, NPC interaction, and sounds.
    """

    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        # Initial player sprite
        self.set_image(self.load_image("Player_right.png"), 200, 200)
        self.handle_key_events = True
        self.register_collision_object("NPC")

        # Persist total_friends
        if not hasattr(Globals, "total_friends"):
            Globals.total_friends = 0
        self.total_friends = Globals.total_friends

        self._in_npc_collision = False

    def _force_set_background(self, image_name):
        # Reload background from disk
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.normpath(os.path.join(base_dir, "..", "images"))
        full_path = os.path.join(images_dir, image_name)
        self.room.background_image = pygame.image.load(full_path).convert()
        self.room.set_background_image(image_name)

    def _set_player_image(self, filename):
        # Change sprite, keep position
        image = self.load_image(filename)
        old_center = self.rect.center
        self.set_image(image, 200, 200)
        self.rect.width, self.rect.height = 150, 150
        self.rect.center = old_center

    def _get_colliding_npc(self):
        for obj in self.room.objects:
            if isinstance(obj, NPC) and self.rect.colliderect(obj.rect):
                return obj
        return None

    def key_pressed(self, key):
        """Handles all player key movement and NPC interactions."""
        distance = 60 if key[pygame.K_LSHIFT] else 30
        moved = False

        # Movement
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
        print(self.x, self.y)

        # NPC interaction ("Y" to befriend, "N" to decline)
        npc = self._get_colliding_npc()
        if npc and key[pygame.K_y] and not getattr(npc, "interacted", False):
            npc.interacted = True
            score_increased = False
            if hasattr(npc, "score_value") and hasattr(self.room, "score") and self.total_friends < 4:
                self.room.score.update_score(npc.score_value)
                self.total_friends += 1
                Globals.total_friends = self.total_friends
                print(self.total_friends)
                score_increased = True

            # Play sounds only if befriending
            if score_increased:
                if hasattr(npc, "npc_type") and npc.npc_type == "nice_friend":
                    try:
                        npc.nice_friend.play()
                    except Exception as e:
                        print("Sound playback error:", e)
                elif hasattr(npc, "npc_type") and npc.npc_type == "creep":
                    try:
                        print(f"Playing creep sound: {getattr(npc.sound_to_play, 'name', npc.sound_to_play)}")
                        npc.sound_to_play.set_volume(1.0)
                        npc.sound_to_play.play()
                    except Exception as e:
                        print("Sound playback error (creep):", e)
            elif self.total_friends >= 4 and hasattr(self.room, "friend_text"):
                self.room.friend_text.text = "You've already made 4 friends! I guess I can't friend you..."
                self.room.friend_text.render_text()

        elif npc and key[pygame.K_n] and not getattr(npc, "interacted", False):
            npc.interacted = True
            if hasattr(self.room, "friend_text"):
                self.room.friend_text.text = "Maybe next time!"
                self.room.friend_text.render_text()

            if hasattr(npc, "worthyness") and hasattr(self.room, "score"):
                self.room.score.update_score(npc.worthyness)

        self._handle_room_transitions()

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

    def Keep_In_Room(self):
        w, h = self.room.screen.get_width(), self.room.screen.get_height()
        self.x = max(160, min(self.x, 1560))
        self.y = max(100, min(self.y, 780))

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

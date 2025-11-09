from GameFrame import RoomObject, Globals
import pygame
import time
from Objects.Hud import MenuList, Text
from random import choice

class Messenger(RoomObject):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        image = self.load_image("Phone.png")
        self.set_image(image, 1920, 1080)
        self.handle_key_events = True
        self.handle_mouse_events = False

        self.feedback_text = None
        self.reported_friends = {}
        self.blocked_friends = {}
        self.last_key_time = 0
        self.key_delay = 0.3
        self.last_message_was_friendly = False

        self.option_positions = {
            "New_friend1": (800, 400),
            "New_friend2": (800, 600),
            "New_friend3": (800, 780),
            "New_friend4": (800, 900),
        }

        self.friendly_texts = [
            "Hey dude, we should totally chat more often!",
            "You seem like a chill guy lol",
            "Yo we should be good friends bro"
        ]

        bad_text = 20
        good_text = -50
        self.messages = [
            ("Hey, there's this loser that we totally should make fun of!", bad_text),
            ("Dude, we GOTTA cyberbully this guy", bad_text),
            ("We need to cyberbully this guy, it'll be hilarious.", bad_text),
            ("Let's spam their inbox until they quit.", bad_text),
            ("We should make a meme about how dumb they are.", bad_text),
            ("Hey dude, we should totally chat more often!", good_text),
            ("You seem like a chill guy lol", good_text),
            ("Yo we should be good friends bro", good_text)
        ]

        self.last_msg = None
        self.last_msg_score = 0

        self.menu = MenuList(
            room, 1720 // 2, 300,
            ["New_friend1", "---", "---", "---",
             "New_friend2", "---", "---", "---",
             "New_friend3", "---", "---", "---",
             "New_friend4"]
        )
        room.add_room_object(self.menu)
        room.messenger = self

    def key_pressed(self, key):
        now = time.time()
        if now - self.last_key_time < self.key_delay:
            return

        if key[pygame.K_ESCAPE]:
            for level_name in ["Path", "School_Pathway"]:
                if level_name in Globals.levels:
                    Globals.next_level = Globals.levels.index(level_name)
                    break
            self.last_key_time = now
            self.room.done = True
            print("Exiting Messenger and returning to previous room")

        elif key[pygame.K_RETURN]:
            selected = self.menu.items[self.menu.selected_index]
            pos = self.option_positions.get(selected, (1720 // 2, 800))
            self._clear_feedback_text()
            friend_map = {
                1: ["New_friend1"],
                2: ["New_friend1", "New_friend2"],
                3: ["New_friend1", "New_friend2", "New_friend3"],
                4: ["New_friend1", "New_friend2", "New_friend3", "New_friend4"]
            }
            all_friends = set(sum(friend_map.values(), []))

            # reset friendly text flag
            self.last_message_was_friendly = False

            if Globals.total_friends == 0 or selected not in all_friends:
                msg = "You have no friends!"
                score_val = 0
            elif Globals.total_friends in friend_map:
                allowed_friends = friend_map[Globals.total_friends]
                if selected in allowed_friends:
                    msg, score_val = choice(self.messages)
                    # Set flag if a friendly text was displayed
                    if msg in self.friendly_texts:
                        self.last_message_was_friendly = True
                    else:
                        self.last_message_was_friendly = False
                else:
                    msg = f"You only have {Globals.total_friends} friend(s)!"
                    score_val = 0
            else:
                msg, score_val = choice(self.messages)
                if msg in self.friendly_texts:
                    self.last_message_was_friendly = True
                else:
                    self.last_message_was_friendly = False

            self._set_feedback_text(Text(self.room, pos[0], pos[1], msg))
            self.last_msg = msg
            self.last_msg_score = score_val
            self.last_key_time = now

        elif key[pygame.K_w]:
            self.menu.move_selection(-1)
            self._clear_feedback_text()
            self.last_key_time = now

        elif key[pygame.K_s]:
            self.menu.move_selection(1)
            self._clear_feedback_text()
            self.last_key_time = now

    def _clear_feedback_text(self):
        if self.feedback_text:
            self.room.delete_object(self.feedback_text)
            self.feedback_text = None

    def _set_feedback_text(self, text_obj):
        self.feedback_text = text_obj
        self.feedback_text.depth = 1
        self.room.add_room_object(self.feedback_text)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

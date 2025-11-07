from GameFrame import RoomObject, Globals
import pygame
import time
from Objects.Hud import MenuList, Text

class Messenger(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        image = self.load_image("Phone.png")
        self.set_image(image, 1920, 1080)
        self.handle_key_events = True

        self.feedback_text = None

        # cooldown tracking
        self.last_key_time = 0
        self.key_delay = 0.3  # seconds between accepted key presses

        # positions for each option
        self.option_positions = {
            "New_friend1": (800, 400),
            "New_friend2": (800, 600),
            "New_friend3": (800, 780),
            "New_friend4": (800, 900),
        }

        self.menu = MenuList(
            room, 1720//2, 300,
            ["New_friend1","---","---","---",
             "New_friend2","---","---","---",
             "New_friend3","---","---","---",
             "New_friend4"]
        )
        room.add_room_object(self.menu)

    def key_pressed(self, key):
        now = time.time()
        if now - self.last_key_time < self.key_delay:
            return  # ignore if still in cooldown

        if key[pygame.K_ESCAPE]:
            if "Path" in Globals.levels:
                Globals.next_level = Globals.levels.index("Path")
            elif "School_Pathway" in Globals.levels:
                Globals.next_level = Globals.levels.index("School_Pathway")
            self.room.done = True
            print("Exiting Messenger and returning to previous room")
            self.last_key_time = now

        elif key[pygame.K_RETURN]:
            # toggle feedback text
            if self.feedback_text:
                self.room.delete_object(self.feedback_text)
                self.feedback_text = None
                print("Feedback text cleared")
            else:
                selected = self.menu.items[self.menu.selected_index]
                print(f"Selected menu item: {selected}")

                # look up position for this option, fallback to center
                pos = self.option_positions.get(selected, (1720//2, 800))

                self.feedback_text = Text(self.room, pos[0], pos[1], f"You selected {selected}")
                self.feedback_text.depth = 1
                self.room.add_room_object(self.feedback_text)
                print("Feedback text created")
            self.last_key_time = now

        elif key[pygame.K_w]:
            self.menu.move_selection(-1)
            if self.feedback_text:
                self.room.delete_object(self.feedback_text)
                self.feedback_text = None
            self.last_key_time = now

        elif key[pygame.K_s]:
            self.menu.move_selection(1)
            if self.feedback_text:
                self.room.delete_object(self.feedback_text)
                self.feedback_text = None
            self.last_key_time = now

    def draw(self, surface):
        surface.blit(self.image, self.rect)

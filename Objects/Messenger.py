from GameFrame import RoomObject, Globals
import pygame
from Objects.Hud import MenuList, Text   # make sure Text is imported

class Messenger(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        image = self.load_image("Phone.png")
        self.set_image(image, 1920, 1080)
        self.handle_key_events = True

        # Add interactive list
        self.menu = MenuList(
            room, 1720/2, 300,
            ["New_friend1","---","---","---",
             "New_friend2","---","---","---",
             "New_friend3","---","---","---",
             "New_friend4"]
        )
        room.add_room_object(self.menu)

        # placeholder for feedback text
        self.feedback_text = None

    def key_pressed(self, key):
        if key[pygame.K_ESCAPE]:
            if "Path" in Globals.levels:
                Globals.next_level = Globals.levels.index("Path")
            elif "School_Pathway" in Globals.levels:
                Globals.next_level = Globals.levels.index("School_Pathway")
            self.room.done = True
            print("Exiting Messenger and returning to previous room")

        elif key[pygame.K_RETURN]:
            selected = self.menu.items[self.menu.selected_index]
            print(f"Selected menu item: {selected}")

            self.feedback_text = Text(self.room, 1720//2, 800, f"You selected {selected}")
            self.feedback_text.depth = 1  # ensure it draws above background
            self.room.add_room_object(self.feedback_text)


    def draw(self, surface):
        surface.blit(self.image, self.rect)

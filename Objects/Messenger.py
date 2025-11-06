from GameFrame import RoomObject, Globals
import pygame
from Objects.Hud import MenuList

class Messenger(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        image = self.load_image("Phone.png")
        self.set_image(image, 1920, 1080)
        self.handle_key_events = True

        # Add interactive list
        self.menu = MenuList(room, 1720/2, 300, ["New_friend1","---","---","---" ,"New_friend2","---","---","---" , "New_friend3","---","---","---" , "New_friend4"])
        room.add_room_object(self.menu)

    def key_pressed(self, key):
        if key[pygame.K_ESCAPE]:
            if "Path" in Globals.levels:
                Globals.next_level = Globals.levels.index("Path")
            elif "School_Pathway" in Globals.levels:
                Globals.next_level = Globals.levels.index("School_Pathway")
            self.room.done = True
            print("Exiting Messenger and returning to previous room")

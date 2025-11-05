from GameFrame import RoomObject, Globals
import pygame

class Messenger(RoomObject):
    """
    The object for displaying the title
    """
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        
        # set image
        image = self.load_image("Phone.png")
        self.set_image(image,1920,1080)
        
        # register for key events
        self.handle_key_events = True 
        
    def key_pressed(self, key):
        if key[pygame.K_ESCAPE]:
            # End this room and go back to Path (or School_Pathway)
            if "Path" in Globals.levels:
                Globals.next_level = Globals.levels.index("Path")
            elif "School_Pathway" in Globals.levels:
                Globals.next_level = Globals.levels.index("School_Pathway")

            self.room.done = True
            print("Exiting Messenger and returning to previous room")

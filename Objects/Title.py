from GameFrame import RoomObject, Globals
from Objects.Hud import Timer
import pygame
from sys import exit

class Title(RoomObject):
    """
    The object for displaying the title
    """
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        image = self.load_image("Title.png")
        self.set_image(image,1920,1080)
        self.handle_key_events = True 

    def key_pressed(self, key):
        """
        If the key pressed is space the game will start
        """
        if key[pygame.K_SPACE]:
            # Start the timer
            if not hasattr(Globals, "game_timer") or Globals.game_timer is None:
                Globals.game_timer = Timer(self.room, 1400, 50, 150)  # Or (100,100) if you prefer top-left
            self.room.timer = Globals.game_timer
            self.room.timer.room = self.room
            self.room.add_room_object(self.room.timer)
            # Proceed to next level or start flag here, e.g.:
            self.room.running = False    # Or trigger next level transition here

        elif key[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

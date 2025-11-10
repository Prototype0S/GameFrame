from GameFrame import Level
import pygame
from Objects.Hud import ExitOnTimer  # import the new timer object

class Failure(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        self.set_background_image("failure.png")
        pygame.mixer.stop()
        self.bg_music = self.load_sound("failure.wav")
        self.bg_music.set_volume(0.5)
        self.bg_music.play(loops=1)
        # Add the room object that will close game after 5s
        self.add_room_object(ExitOnTimer(self, 5))

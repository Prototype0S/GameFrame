from GameFrame import Level
from Objects.Hud import ExitOnTimer
import pygame
class Victory(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        self.set_background_image("victory.png")
        # stop any other audios
        pygame.mixer.stop()
        
        # load sounds
        self.bg_music = self.load_sound("victory.wav")
        self.bg_music.set_volume(0.5)
        
        # play background music
        self.bg_music.play(loops=1)
        # Add the room object that will close game after 5s
        self.add_room_object(ExitOnTimer(self, 5))

        

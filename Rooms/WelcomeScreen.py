from GameFrame import Level
from Objects.Title import Title
import pygame

class WelcomeScreen(Level):
    """
    Intial screen for the game
    """
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        
        # set background image
        self.set_background_image("Title.png")
        
        # add title object
        self.add_room_object(Title(self, 1920, 1080))
        #stop any other audios
        pygame.mixer.stop()
        # load sounds
        self.bg_music = self.load_sound("background_music.mp3")
        self.bg_music.set_volume(0.5)
        # play background music
        self.bg_music.play(loops=1)
    
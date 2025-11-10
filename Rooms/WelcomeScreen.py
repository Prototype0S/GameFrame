from GameFrame import Level, Globals
from Objects.Title import Title
from Objects.Hud import Timer
import pygame

class WelcomeScreen(Level):
    """
    Initial screen for the game
    """
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        
        # set background image
        self.set_background_image("Title.png")
        
        # add title object
        self.add_room_object(Title(self, 1920, 1080))
        
        # stop any other audios
        pygame.mixer.stop()
        
        # load sounds
        self.bg_music = self.load_sound("background_music.mp3")
        self.bg_music.set_volume(0.5)
        
        # play background music
        self.bg_music.play(loops=1)
        
        # Timer logic: create/persist and always add as RoomObject
        if not hasattr(Globals, "game_timer") or Globals.game_timer is None:
            Globals.game_timer = Timer(self, 1400, 50, 150)  # 2 min 30s
        
        self.timer = Globals.game_timer
        self.timer.room = self  # update .room reference for drawing
        self.add_room_object(self.timer)

from GameFrame import Level, Globals
from Objects.Messenger import Messenger
from Objects.Report_button import Report_button
from Objects.Block_button import Block_button
from Objects.Hud import Score, Timer
import pygame


class Phone(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        self.score = Score(self, 800, 200)
        self.add_room_object(self.score)
        self.set_background_image("Background.png")
        self.add_room_object(Messenger(self, 0, 100))
        
        self.add_room_object(Report_button(self, 1080, 150))
        self.add_room_object(Block_button (self,1180, 150))
        if not hasattr(Globals, "game_timer") or Globals.game_timer is None:
            Globals.game_timer = Timer(self, 200, 100, 180)  # x=100, y=100, duration=180s

        self.timer = Globals.game_timer
        self.timer.room = self
        self.timer.x = 200
        self.timer.y = 100
        self.add_room_object(self.timer)
        self.timer.depth = 20  # Make sure it's drawn on top if there's any HUD layering

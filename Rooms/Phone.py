from GameFrame import Level
from Objects.Messenger import Messenger
from Objects.Report_button import Report_button
import pygame


class Phone(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        self.set_background_image("Background.png")
        self.add_room_object(Messenger(self, 0, 100))
        self.add_room_object(Report_button(self, 900, 500))

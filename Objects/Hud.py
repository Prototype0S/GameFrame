from GameFrame import RoomObject, Globals
from random import choice
import pygame

class Score(RoomObject):
    """
    Score display as a RoomObject so GameFrame draws it automatically.
    """
    def __init__(self, room, x, y, text=None):
        RoomObject.__init__(self, room, x, y)

        self.x = x
        self.y = y
        self.text = str(text if text is not None else Globals.SCORE)
        self.size = 60
        self.font_name = "Arial Black"
        self.color = (0, 0, 0)
        self.bold = False

        self._render_score()

    def _render_score(self):
        """Render text to a surface so GameFrame can draw it like a RoomObject."""
        font = pygame.font.SysFont(self.font_name, self.size, self.bold)
        self.image = font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update_score(self, change):
        """Update the score and refresh the image."""
        Globals.SCORE += change
        self.text = str(Globals.SCORE)
        self._render_score()

class Text(RoomObject):
    def __init__(self, room, x, y, text=None):
        RoomObject.__init__(self, room, x, y)

        self.x = x
        self.y = y
        self.text = str(text if text is not None else Globals.SCORE)
        self.size = 60
        self.font_name = "Arial Black"
        self.color = (0, 0, 0)
        self.bold = False
        self.render_text()
    def render_text(self):
        font = pygame.font.SysFont(self.font_name, self.size, self.bold)
        self.image = font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update_text(self):
        self.text = choice(["Hi, let's be friends!", "Hello there!", "Good day!", "Hey! Wanna hang out?", "Wanna be friends?", "Yo! Let's be pals!"])
        self.render_text()
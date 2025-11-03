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
        # store numeric score, not prefixed string
        self.value = Globals.SCORE if text is None else int(text)
        self.size = 60
        self.font_name = "Arial Black"
        self.color = (0, 255, 255)
        self.bold = False

        self._render_score()

    def _render_score(self):
        """Render text to a surface so GameFrame can draw it like a RoomObject."""
        font = pygame.font.SysFont(self.font_name, self.size, self.bold)
        display_text = f"Score: {self.value}"
        self.image = font.render(display_text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update_score(self, change):
        """Update the score and refresh the image."""
        Globals.SCORE += change
        self.value = Globals.SCORE
        self._render_score()

class Text(RoomObject):
    def __init__(self, room, x, y, text=None):
        RoomObject.__init__(self, room, x, y)

        self.x = x
        self.y = y
        self.text = str(text if text is not None else "")
        self.size = 30
        self.font_name = "Arial Black"
        self.color = (0, 0, 0)
        self.bold = False
        self.render_text()
    def render_text(self):
        font = pygame.font.SysFont(self.font_name, self.size, self.bold)
        self.image = font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update_text(self):
        self.text = choice(["Hi, let's be friends!", "Hey! Wanna hang out sometime?", "Wanna be friends?", "Yo! Let's be pals!", "Sup! Let's chill together!", "Hey there! Let's connect!", "Let's be buddies!", "Hi! Let's team up!", "Yo! Let's be amigos!"])
        self.render_text()
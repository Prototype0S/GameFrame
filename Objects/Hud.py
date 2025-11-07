from GameFrame import RoomObject, Globals
import pygame
import time
from random import choice

class Score(RoomObject):
    def __init__(self, room, x, y, text=None):
        RoomObject.__init__(self, room, x, y)
        self.x = x
        self.y = y
        self.value = Globals.SCORE if text is None else int(text)
        self.size = 60
        self.font_name = "Arial Black"
        self.color = (0, 255, 255)
        self.bold = False
        self._render_score()

    def _render_score(self):
        font = pygame.font.SysFont(self.font_name, self.size, self.bold)
        display_text = f"Score: {self.value}"
        self.image = font.render(display_text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update_score(self, change):
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
        self.text = choice([
            "Hi, let's be friends!",
            "Hey! Wanna hang out sometime?",
            "Wanna be friends?",
            "Yo! Let's be pals!",
            "Sup! Let's chill together!",
            "Hey there! Let's connect!",
            "Let's be buddies!",
            "Hi! Let's team up!",
            "Yo! Let's be amigos!"
        ])
        self.render_text()


class MenuList(RoomObject):
    def __init__(self, room, x, y, items):
        RoomObject.__init__(self, room, x, y)
        self.x = x
        self.y = y
        self.items = items
        self.selected_index = 0

        self.size = 36
        self.font_name = "Arial Black"
        self.color = (200, 200, 200)
        self.highlight_color = (0, 255, 255)
        self.bold = False

        # Messenger will handle keys, not MenuList
        self.handle_key_events = False

        self._render_items()

    def _render_items(self):
        font = pygame.font.SysFont(self.font_name, self.size, self.bold)
        line_height = self.size + 10
        widths = [font.size(str(text))[0] for text in self.items if text not in (None, "---")]
        width = max(widths) if widths else 100
        height = line_height * len(self.items)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        self.images = []
        for i, text in enumerate(self.items):
            color = self.highlight_color if i == self.selected_index else self.color
            display = "" if text in (None, "---") else str(text)
            img = font.render(display, True, color)
            rect = img.get_rect(topleft=(0, i * line_height))
            self.images.append((img, rect))
            self.image.blit(img, rect.topleft)

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move_selection(self, direction):
        if not self.items:
            return
        while True:
            self.selected_index = (self.selected_index + direction) % len(self.items)
            if self.items[self.selected_index] not in (None, "---"):
                break
        self._render_items()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

from GameFrame import RoomObject, Globals
import pygame
from random import choice
import time


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
    """
    Simple text display object.
    """
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
    """
    A vertical interactive list navigable with W/S keys.
    Supports spacers (None or '---') which are drawn but skipped in selection.
    Includes a cooldown so keys can't cycle too quickly.
    """
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

        self.handle_key_events = True

        # cooldown tracking
        self.last_move_time = 0
        self.move_delay = 0.2  # seconds

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
            # pick highlight color if this is the selected item, otherwise normal color
            color = self.highlight_color if i == self.selected_index else self.color

            # render spacers as blanks, everything else as text
            display = "" if text in (None, "---") else str(text)
            img = font.render(display, True, color)

            rect = img.get_rect(topleft=(0, i * line_height))
            self.images.append((img, rect))
            self.image.blit(img, rect.topleft)


        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def _move_selection(self, direction):
        while True:
            self.selected_index = (self.selected_index + direction) % len(self.items)
            if self.items[self.selected_index] not in (None, "---"):
                break

    def key_pressed(self, key):
        now = time.time()
        if now - self.last_move_time < 0.5:
            return  # ignore if still in cooldown

        if key[pygame.K_w]:
            self._move_selection(-1)
            self._render_items()
            self.last_move_time = now
        elif key[pygame.K_s]:
            self._move_selection(1)
            self._render_items()
            self.last_move_time = now
        elif key[pygame.K_RETURN]:
            selected = self.items[self.selected_index]
            
            if now - self.last_move_time < self.move_delay:
                return  # ignore if still in cooldown
            print(f"Selected menu item: {selected}")
            # Hook in your action here

    def draw(self, surface):
        surface.blit(self.image, self.rect)
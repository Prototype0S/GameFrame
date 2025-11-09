from GameFrame import RoomObject, Globals
from Objects.Hud import Text
import pygame
import os

class Block_button(RoomObject):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        self.handle_mouse_events = True
        self.depth = 9

        image = self.load_image("block_button.png")
        self.set_image(image, 100, 70)
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        if self not in room.mouse_objects:
            room.mouse_objects.append(self)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        sounds_dir = os.path.normpath(os.path.join(base_dir, "..", "Sounds"))
        self.friendly_blocked = pygame.mixer.Sound(os.path.join(sounds_dir, "friendly_blocked.wav"))

    def clicked(self, button_number):
        if button_number == 1:
            messenger = getattr(self.room, "messenger", None)
            score_obj = getattr(self.room, "score", None)
            if messenger and score_obj:
                messenger._clear_feedback_text()
                selected_friend = messenger.menu.items[messenger.menu.selected_index]
                if messenger.blocked_friends.get(selected_friend, False):
                    print(f"{selected_friend} already blocked! Clearing text.")
                    messenger._clear_feedback_text()
                else:
                    score_val = messenger.last_msg_score
                    score_obj.update_score(score_val)
                    print(f"Score updated by {score_val} due to message: {messenger.last_msg}")
                    messenger.blocked_friends[selected_friend] = True
                    messenger._set_feedback_text(Text(
                        self.room, 900, 100, f"{selected_friend} blocked!"
                    ))
                    if getattr(messenger, "last_message_was_friendly", False):
                        try:
                            self.friendly_blocked.play()
                        except Exception as e:
                            print("Sound playback error (friendly_blocked):", e)
                    Globals.total_friends -= 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 3)

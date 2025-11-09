import pygame
import os
from GameFrame import RoomObject
from random import choice

class NPC(RoomObject):
    def __init__(self, room, x, y, npc_type):
        super().__init__(room, x, y)
        self.npc_type = npc_type  # "creep" or "nice_friend"
        sprite = "Creep.png" if npc_type == "creep" else "Skater.png"
        image = self.load_image(sprite)
        self.set_image(image, 225, 225)
        self.register_collision_object("Player")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        sounds_dir = os.path.normpath(os.path.join(base_dir, "..", "Sounds"))
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.creep1 = pygame.mixer.Sound(os.path.join(sounds_dir, "creep1.wav"))
        self.creep2 = pygame.mixer.Sound(os.path.join(sounds_dir, "creep2.wav"))
        self.nice_friend = pygame.mixer.Sound(os.path.join(sounds_dir, "power_up.mp3"))

        # Assign correct sound and score values
        if npc_type == "creep":
            self.score_value = 5
            self.worthyness = 10
            self.sound_to_play = choice([self.creep1, self.creep2])
        else:
            self.score_value = 50
            self.worthyness = 0
            self.sound_to_play = self.nice_friend

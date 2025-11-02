from GameFrame import RoomObject
from random import choice

class NPC(RoomObject):
    def __init__(self, room, x, y):
        # Explicit RoomObject init
        RoomObject.__init__(self, room, x, y)
        sprite = choice(["Creep.png", 'Skater.png'])
        image = self.load_image(sprite)
        self.set_image(image, 225, 225)
        self.register_collision_object("Player")



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
        
        if sprite == "Creep.png":
            self.score_value = 5
            #will add score by 10 if player declines
            self.worthyness = 10
        else:
            self.score_value = 50



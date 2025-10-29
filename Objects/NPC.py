from GameFrame import RoomObject

class NPC(RoomObject):
    def __init__(self, room, x, y):
        # Explicit RoomObject init
        RoomObject.__init__(self, room, x, y)

        image = self.load_image("Creep.png")
        self.set_image(image, 250, 250)
        self.register_collision_object("Player")



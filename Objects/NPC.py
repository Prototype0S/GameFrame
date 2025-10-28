from GameFrame import RoomObject

class NPC(RoomObject):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        image = self.load_image("Creep.png")
        self.set_image(image, 250, 250)
        self.register_collision_object("Player")

    def handle_collision(self, other, other_type):
        # Respond to collisions with the player
        if other_type == "Player" or getattr(other, "__class__", type(other)).__name__ == "Player":
            print("NPC collided with Player — changing background")
            self.room.set_background_image("Text_Path.png")
            self.room.create_banner = False

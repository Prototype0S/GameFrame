from GameFrame import RoomObject

class NPC(RoomObject):
    def __init__(self, room, x, y):
        # Explicit RoomObject init
        RoomObject.__init__(self, room, x, y)

        image = self.load_image("Creep.png")
        self.set_image(image, 250, 250)
        self.register_collision_object("Player")

    def handle_collision(self, other, other_type):
        # Only react to collisions with the player
        if other_type == "Player" or getattr(other, "__class__", type(other)).__name__ == "Player":
            if type(self.room).__name__ == "Path":
                self.room.set_background_image("Text_Path.png")
                self.room.create_banner = False
            elif type(self.room).__name__ == "School_Pathway":
                self.room.set_background_image("School_Path_text.png")
                self.room.create_banner = False

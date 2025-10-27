from GameFrame import RoomObject
#from Text_banner_creation import Text_banner_creation  # Import your banner class

class NPC(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)

        image = self.load_image("Creep.png")
        self.set_image(image, 250, 250)

    #    self.register_collision_object("Player")

    #def handle_collision(self, other, other_type):
    #    if other_type == "Player":
    #        # Create banner object and add it to the room
    #        banner = Text_banner_creation(self.room, 0, self.room.screen.get_height() - 300)
    #        self.room.add_room_object(banner)

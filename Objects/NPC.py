from GameFrame import RoomObject


class NPC(RoomObject):
    """
    The object for displaying the title
    """
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        
        # set image
        image = self.load_image("Creep.png")
        self.set_image(image,250,250)
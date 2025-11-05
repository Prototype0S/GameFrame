from GameFrame import Level
from Objects.Messenger import Messenger

class Phone(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        
        # set background image
        self.set_background_image("Phone.png")
        
        # add title object
        self.add_room_object(Messenger(self, 1920, 1080))
from GameFrame import Level
from Objects.Messenger import Messenger

class Phone(Level):
    def __init__(self, screen, joysticks):
        # call parent constructor explicitly
        Level.__init__(self, screen, joysticks)
        
        # set background image
        self.set_background_image("Background.png")
        
        # add Messenger object
        self.add_room_object(Messenger(self, 0, 100))
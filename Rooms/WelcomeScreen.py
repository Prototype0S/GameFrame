from GameFrame import Level
from Objects.Title import Title

class WelcomeScreen(Level):
    """
    Intial screen for the game
    """
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        
        # set background image
        self.set_background_image("Title.png")
        
        # add title object
        self.add_room_object(Title(self, 1920, 1080))
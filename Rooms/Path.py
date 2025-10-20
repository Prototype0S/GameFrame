
from GameFrame import Level, Globals
from Objects.Player import Player

class Path(Level):
    def __init__(self, screen, joysticks):
        super().__init__(screen, joysticks)

        self.set_background_image("Path.png")
        self.player = Player(self, 400, 500)
        self.add_room_object(self.player)

        # Required for transition
        self.done = False
        self.next_level_class = None

    def request_room_change(self, target_room_name):
        print(f"Requesting room change to: {target_room_name}")  # Debug
        # Use the level name lookup to avoid importing the other room module
        if target_room_name == "School_Pathway" and "School_Pathway" in Globals.levels:
            Globals.next_level = Globals.levels.index("School_Pathway")
            self.done = True
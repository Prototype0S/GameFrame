from GameFrame import Level, Globals
from Objects.Player import Player
class School_Pathway(Level):
    def __init__(self, screen, joysticks, x=400, y=500):
        super().__init__(screen, joysticks)
        self.set_background_image("School_Path.png")
        self.player = Player(self, x, y)
        self.add_room_object(self.player)

    def request_room_change(self, target_room_name):
        print(f"Requesting room change to: {target_room_name}")  # Debug
        # Use the level name lookup to avoid importing the other room module
        if target_room_name == "Path" and "Path" in Globals.levels:
            Globals.next_level = Globals.levels.index("Path")
            self.done = True


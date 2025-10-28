from GameFrame import Level, Globals
from Objects.Player import Player
from Objects.NPC import NPC
import random

class Path(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)

        # Default background
        self.set_background_image("Path.png")
        self.create_banner = False

        # Add player
        self.player = Player(self, 300, 500)
        self.add_room_object(self.player)

        # NPC positions (cached in Globals)
        if not hasattr(Globals, "path_npc_positions"):
            Globals.path_npc_positions = {}

        if "Path" in Globals.path_npc_positions:
            positions = Globals.path_npc_positions["Path"]
        else:
            x_vals = [500, 800, 1100, 1400]
            y_vals = [100, 400, 750]
            random.shuffle(x_vals)
            random.shuffle(y_vals)
            positions = list(zip(x_vals[:3], y_vals[:3]))
            Globals.path_npc_positions["Path"] = positions
            print("NPC positions:", positions)

        # Spawn NPCs
        for x, y in positions:
            npc = NPC(self, x, y)
            self.add_room_object(npc)

    def request_room_change(self, target_room_name):
        print(f"Requesting room change to: {target_room_name}")
        if target_room_name == "School_Pathway" and "School_Pathway" in Globals.levels:
            Globals.next_level = Globals.levels.index("School_Pathway")
            self.done = True

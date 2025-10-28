from GameFrame import Level, Globals
from Objects.Player import Player
from Objects.NPC import NPC
import random

class School_Pathway(Level):
    def __init__(self, screen, joysticks, x=400, y=500):
        Level.__init__(self, screen, joysticks)

        # Default background
        self.set_background_image("School_Path.png")
        self.create_banner = False

        # Add player
        self.player = Player(self, x, y)
        self.add_room_object(self.player)

        # NPC positions (cached in Globals)
        if not hasattr(Globals, "School_Pathway_npc_positions"):
            Globals.School_Pathway_npc_positions = {}

        if "School_Pathway" in Globals.School_Pathway_npc_positions:
            positions = Globals.School_Pathway_npc_positions["School_Pathway"]
        else:
            x_vals = [700, 1000]
            y_vals = [100, 500, 750]
            random.shuffle(x_vals)
            random.shuffle(y_vals)
            positions = list(zip(x_vals[:2], y_vals[:2]))
            Globals.School_Pathway_npc_positions["School_Pathway"] = positions
            print("NPC positions:", positions)

        # Spawn NPCs
        for x, y in positions:
            npc = NPC(self, x, y)
            self.add_room_object(npc)

    def request_room_change(self, target_room_name):
        print(f"Requesting room change to: {target_room_name}")
        if target_room_name == "Path" and "Path" in Globals.levels:
            Globals.next_level = Globals.levels.index("Path")
            self.done = True


from GameFrame import Level, Globals
from Objects.Player import Player
from Objects.NPC import NPC
import random
class Path(Level):
    def __init__(self, screen, joysticks):
        super().__init__(screen, joysticks)

        self.set_background_image("Path.png")
        self.player = Player(self, 300, 500)
        self.add_room_object(self.player)

        # Check if NPC positions are already cached
        if "Path" in Globals.path_npc_positions:
            positions = Globals.path_npc_positions["Path"]
        else:
            x_vals = [500, 800, 1100, 1400]
            y_vals = [100,400, 750]

            # Sample 3 unique positions
            random.shuffle(x_vals)
            random.shuffle(y_vals)
            positions = list(zip(x_vals[:3], y_vals[:3]))
            Globals.path_npc_positions["Path"] = positions
            print("NPC positions:", positions)


        # Spawn NPCs using cached or newly generated positions
        for x, y in positions:
            npc = NPC(self, x, y)
            self.add_room_object(npc)

        self.done = False
        self.next_level_class = None
        self.create_banner = False


    def request_room_change(self, target_room_name):
        print(f"Requesting room change to: {target_room_name}")  # Debug
        # Use the level name lookup to avoid importing the other room module
        if target_room_name == "School_Pathway" and "School_Pathway" in Globals.levels:
            Globals.next_level = Globals.levels.index("School_Pathway")
            self.done = True
    def update(self, dt):
        self.text_banner_creation()
    def text_banner_creation(self):
        if self.create_banner:
            print("Creating text banner background")
            self.set_background_image("Text_Path.png")  # tell GameFrame the new name
            self.load_background()                      # <--  NEW: refresh the cache
            self.create_banner = False
            print("Creating text banner background – flag set, background_changed =", self.background_changed)
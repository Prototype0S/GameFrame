from GameFrame import Level, Globals
from Objects.Player import Player
from Objects.NPC import NPC
from Objects.Hud import Score, Text
import random

class Path(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)

        # Default background
        self.set_background_image("Path.png")
        self.create_banner = False

        # Decide spawn position based on where we came from
        spawn_x, spawn_y = 300, 500  # default
        if len(Globals.level_history) >= 2:
            prev_index = Globals.level_history[-2]
            prev_level_name = Globals.levels[prev_index]
            if prev_level_name == "School_Pathway":
                # e.g. spawn further right if coming from School_Pathway
                spawn_x, spawn_y = 1400, 500

        # Add player at chosen spawn
        self.player = Player(self, spawn_x, spawn_y)
        self.add_room_object(self.player)

        # HUD
        self.score = Score(self, 800, 200)
        self.add_room_object(self.score)

        self.friend_text = Text(self, 1520//2, 850, '')
        self.add_room_object(self.friend_text)

        # NPC positions

        x_vals = [500, 700, 1400]
        y_vals = [100, 400, 750]
        random.shuffle(x_vals)
        random.shuffle(y_vals)
        positions = list(zip(x_vals[:3], y_vals[:3]))
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

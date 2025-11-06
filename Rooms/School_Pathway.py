from GameFrame import Level, Globals
from Objects.Player import Player
from Objects.NPC import NPC
from Objects.Hud import Score, Text
import random

class School_Pathway(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)

        # Default background
        self.set_background_image("School_Path.png")
        self.create_banner = False

        # Add player
        self.player = Player(self, 220, 500)
        self.add_room_object(self.player)
        # add HUD items
        self.score = Score(self, 800, 200)
        self.add_room_object(self.score)

        self.friend_text = Text(self, 1520/2, 850, '')
        self.add_room_object(self.friend_text)


        x_vals = [400, 700, 1000]
        y_vals = [100, 500, 750]
        random.shuffle(x_vals)
        random.shuffle(y_vals)
        positions = list(zip(x_vals[:2], y_vals[:2]))

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

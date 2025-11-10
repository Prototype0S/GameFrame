from GameFrame import Level, Globals
from Objects.Player import Player
from Objects.NPC import NPC
from Objects.Hud import Score, Text, Timer
import random

class Path(Level):
    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        self.set_background_image("Path.png")
        self.create_banner = False

        spawn_x, spawn_y = 300, 500
        if len(Globals.level_history) >= 2:
            prev_index = Globals.level_history[-2]
            prev_level_name = Globals.levels[prev_index]
            if prev_level_name == "School_Pathway":
                spawn_x, spawn_y = 1400, 500

        self.player = Player(self, spawn_x, spawn_y)
        self.add_room_object(self.player)
        self.score = Score(self, 800, 200)
        self.add_room_object(self.score)
        self.friend_text = Text(self, 1520//2, 850, '')
        self.add_room_object(self.friend_text)

        # --- Always add the timer and update its room/position ---
        if not hasattr(Globals, "game_timer") or Globals.game_timer is None:
            Globals.game_timer = Timer(self, 200, 100, 180)  # x=100, y=100, duration=180s

        self.timer = Globals.game_timer
        self.timer.room = self
        self.timer.x = 200
        self.timer.y = 100
        self.add_room_object(self.timer)
        self.timer.depth = 20  # Make sure it's drawn on top if there's any HUD layering

        x_vals = [500, 700, 1400]
        y_vals = [100, 400, 750]
        random.shuffle(x_vals)
        random.shuffle(y_vals)
        positions = list(zip(x_vals[:3], y_vals[:3]))
        print("NPC positions:", positions)

        # Randomly assign type to each NPC
        types = [random.choice(["creep", "nice_friend"]) for _ in positions]
        for (x, y), npc_type in zip(positions, types):
            npc = NPC(self, x, y, npc_type)
            self.add_room_object(npc)

    def request_room_change(self, target_room_name):
        print(f"Requesting room change to: {target_room_name}")
        if target_room_name == "School_Pathway" and "School_Pathway" in Globals.levels:
            Globals.next_level = Globals.levels.index("School_Pathway")
            self.done = True

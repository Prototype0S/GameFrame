from GameFrame import RoomObject, Globals
import pygame
import sys

class Player(RoomObject):
    """
    A class for the player's avatar (the Ship)
    """

    def __init__(self,  room: "Path", x, y):
        super().__init__(room, x, y)
        self.room: Path = room  # ✅ Explicit type hint
        image = self.load_image("Ship.png")
        self.set_image(image, 100, 100)

        self.handle_key_events = True

    def key_pressed(self, key):
        distance = 30
        if key[pygame.K_w]:
            self.y -= distance
        elif key[pygame.K_s]:
            self.y += distance
        elif key[pygame.K_a]:
            self.x -= distance
        elif key[pygame.K_d]:
            self.x += distance
        elif key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        self.Keep_In_Room()


        # Trigger room change
        if self.x >= 1500 and hasattr(self.room, "request_room_change") and type(self.room).__name__ == "Path":
                self.room.request_room_change("School_Pathway")
                print(f"Current room: {type(self.room)}")
        # Trigger to go back to previous room using history
        if self.x <= 200 and hasattr(self.room, "request_room_change") and type(self.room).__name__ == "School_Pathway":
            if len(Globals.level_history) >= 2:
                # history[-1] is current room index, history[-2] is previous room index
                prev_index = Globals.level_history[-2]
                Globals.next_level = prev_index
                self.room.done = True
                print(f"DEBUG: Going back to {Globals.levels[prev_index]} (index {prev_index})")
            else:
                # fallback: explicitly go to Path if no history
                if "Path" in Globals.levels:
                    Globals.next_level = Globals.levels.index("Path")
                    self.room.done = True
                    print("DEBUG: No history, falling back to Path")


        #print(self.x, self.y)

    def Keep_In_Room(self):
        if self.x < 190:
            self.x = 190
        if self.y < 100:
            self.y = 100
        if self.x > 1610:
            self.x = 1610
        if self.y > 850:
            self.y = 850

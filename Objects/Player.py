from GameFrame import RoomObject, Globals
import pygame
import sys

class Player(RoomObject):
    """
    A class for the player's avatar (the Ship)
    """

    def __init__(self,  room, x, y):
        super().__init__(room, x, y)
        image = self.load_image("Player_right.png")
        self.set_image(image, 200, 200)

        self.handle_key_events = True
        self.register_collision_object("NPC")
    def key_pressed(self, key):
        distance = 30
        if key[pygame.K_w]:
            image = self.load_image("Player_looking_backwards.png")
            self.set_image(image, 200, 200)
            self.y -= distance
        elif key[pygame.K_s]:
            image = self.load_image("Player_looking_forwards.png")
            self.set_image(image, 200, 200)
            self.y += distance
        elif key[pygame.K_a]:
            image = self.load_image("Player_left.png")
            self.set_image(image, 200, 200)
            self.x -= distance
        elif key[pygame.K_d]:
            image = self.load_image("Player_right.png")
            self.set_image(image, 200, 200)
            self.x += distance
        elif key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        else:
            image = self.load_image("Player_looking_forwards.png")
            self.set_image(image, 200, 200)

        self.Keep_In_Room()
        #print(f"Player position: ({self.x}, {self.y})")


        # Trigger room change
        if self.x >= 1500 and hasattr(self.room, "request_room_change") and type(self.room).__name__ == "Path":
                prev_index =Globals.level_history[-1]
                Globals.next_level = prev_index + 1
                self.room.done = True
                print(f"DEBUG: Going back to {Globals.levels[prev_index]} (index {prev_index})")
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
        if self.y > 800:
            self.y = 800

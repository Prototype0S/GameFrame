import os
import math
import pygame
from GameFrame import Level
from typing import List, Tuple, Callable


class RoomObject:
    """
    Base class for all objects that can exist in a game level (Room).

    Provides core functionality for position, movement, image handling, collision detection,
    event handling, and interaction with the game environment.

    Attributes:
        room (Level): The level or room this object belongs to.
        depth (int): Drawing order depth.
        x (int): X-coordinate of the object.
        y (int): Y-coordinate of the object.
        rect (pygame.Rect): The rectangle representing the object's position and size.
        prev_x (int): Previous X-coordinate (for movement/collision).
        prev_y (int): Previous Y-coordinate (for movement/collision).
        width (int): Width of the object.
        height (int): Height of the object.
        image: The current image surface of the object.
        image_orig: The original image surface (for rotation).
        curr_rotation (int): Current rotation angle.
        x_speed (float): Current speed in the X direction.
        y_speed (float): Current speed in the Y direction.
        gravity (float): Gravity applied to the object.
        handle_key_events (bool): Whether the object handles key events.
        handle_mouse_events (bool): Whether the object handles mouse events.
        angle (int): Current angle for movement or rotation.
        collision_object_types (set): Set of object type names to check collisions against.
        collision_objects (list): List of objects to check for collisions.
    """

    def __init__(self, room: Level, x: int, y: int):
        """
        Initializes a RoomObject with position and default properties.

        Args:
            room (Level): The level or room this object belongs to.
            x (int): Initial X-coordinate.
            y (int): Initial Y-coordinate.
        """
        self.room = room
        self.depth = 0
        self.x = x
        self.y = y
        self.rect = 0
        self.prev_x = x
        self.prev_y = y
        self.width = 0
        self.height = 0
        self.image = 0
        self.image_orig = 0
        self.curr_rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0
        self.handle_key_events = False
        self.handle_mouse_events = False
        self.angle = 0

        self.collision_object_types = set()
        self.collision_objects = []

    @staticmethod
    def load_image(file_name: str) -> str:
        """
        Returns the full path to an image file in the Images directory.

        Args:
            file_name (str): Filename of the image.

        Returns:
            str: Full path to the image file.
        """
        return os.path.join('Images', file_name)

    def set_image(self, image: str, width: int, height: int):
        """
        Loads and sets the object's image, scaling to the given width and height.

        Args:
            image (str): Path to the image file.
            width (int): Width to scale the image to.
            height (int): Height to scale the image to.
        """
        self.image_orig = pygame.image.load(image).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (width, height))
        self.width = width
        self.height = height
        self.image = self.image_orig.copy()
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def register_collision_object(self, collision_object: str):
        """
        Registers a type of object for collision detection.

        Args:
            collision_object (str): The class name of the object type to check collisions with.
        """
        self.collision_object_types.add(collision_object)

    def update(self):
        """
        Updates the object's position based on speed and gravity.
        """
        self.y_speed = self.y_speed + self.gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def delete_object(self, obj: 'RoomObject'):
        """
        Removes an object from the level.

        Args:
            obj (RoomObject): The object to remove.
        """
        self.room.delete_object(obj)

    def remove_object(self, obj: 'RoomObject'):
        """
        Removes an object from this object's collision list.

        Args:
            obj (RoomObject): The object to remove from collision_objects.
        """
        for index, list_obj in enumerate(self.collision_objects):
            if list_obj is obj:
                self.collision_objects.pop(index)

    def prestep(self):
        """
        Optional: Called before the main step/update logic.
        Override in subclasses for custom behavior.
        """
        pass
    
    def step(self):
        """
        Optional: Called for the main step/update logic.
        Override in subclasses for custom behavior.
        """
        pass

    def check_collisions(self):
        """
        Checks for collisions with registered collision objects and handles them.
        """
        for item in self.collision_objects:
            if self.rect.colliderect(item.rect):
                item_type = type(item).__name__
                self.handle_collision(item, item_type)

    def collides_at(self, obj, x, y, collision_type):
        """
        Checks if moving an object to (x, y) would cause a collision with a given type.

        Args:
            obj (RoomObject): The object to check.
            x (int): X offset.
            y (int): Y offset.
            collision_type (str): The class name of the object type to check against.

        Returns:
            bool: True if a collision would occur, False otherwise.
        """
        check_rect = obj.rect.move(x, y)
        collision_found = False
        for item in self.collision_objects:
            if check_rect.colliderect(item.rect):
                if type(item).__name__ == collision_type:
                    collision_found = True
                    break
        return collision_found

    def handle_collision(self, other, other_type):
        """
        Handles a collision with another object.
        Override in subclasses for custom collision behavior.

        Args:
            other (RoomObject): The other object collided with.
            other_type (str): The class name of the other object.
        """
        pass

    def key_pressed(self, key):
        """
        Handles key press events, if handle_key_events is True.
        Override in subclasses for custom key handling.

        Args:
            key: The pygame key state array.
        """
        pass

    def joy_pad_signal(self, p1_buttons: List[int], p2_buttons: List[int]):
        """
        Handles joystick/gamepad input.
        Override in subclasses for custom joystick handling.

        Args:
            p1_buttons (List[int]): Player 1 button/axis states.
            p2_buttons (List[int]): Player 2 button/axis states.
        """
        pass

    def clicked(self, button_number):
        """
        Handles mouse click events, if handle_mouse_events is True.
        Override in subclasses for custom click handling.

        Args:
            button_number (int): The mouse button number clicked.
        """
        pass

    def mouse_event(self, mouse_x, mouse_y, button_left, button_middle, button_right):
        """
        Handles mouse movement and button events, if handle_mouse_events is True.
        Override in subclasses for custom mouse handling.

        Args:
            mouse_x (int): Mouse X position.
            mouse_y (int): Mouse Y position.
            button_left (bool): Left mouse button state.
            button_middle (bool): Middle mouse button state.
            button_right (bool): Right mouse button state.
        """
        pass

    def bounce(self, other):
        """
        Reverses speed and position if this object bounces off another object.

        Args:
            other (RoomObject): The object to bounce off.
        """

        # self is to the side of other
        if other.rect.top < self.rect.centery < other.rect.bottom:
            self.x_speed *= -1
            self.x = self.prev_x

        # self is above or below other
        if other.rect.left < self.rect.centerx < other.rect.right:
            self.y_speed *= -1
            self.y = self.prev_y

    def blocked(self):
        """
        Stops movement and resets position if the object is blocked.
        """

        self.x = self.prev_x
        self.y = self.prev_y
        self.x_speed = 0
        self.y_speed = 0

    def set_timer(self, ticks: int, function_call: Callable):
        """
        Sets a timed event to call a function after a number of ticks.

        Args:
            ticks (int): Number of frames to wait before calling the function.
            function_call (Callable): The function to call.
        """
        self.room.set_timer(ticks, function_call)

    def set_direction(self, angle: int, speed: int):
        """
        Sets the object's movement direction and speed based on an angle.

        Args:
            angle (int): The angle in degrees.
            speed (int): The speed value.
        """
        self.x_speed = speed * math.cos(math.radians(angle % 360))
        self.y_speed = (speed * math.sin(math.radians(angle % 360))) * -1
        
        """if angle < 0:
            pass
        elif angle == 0:
            self.x_speed = speed
            self.y_speed = 0
        elif angle < 90:
            self.x_speed, self.y_speed = self._get_direction(angle, speed)
        elif angle == 90:
            self.x_speed = 0
            self.y_speed = speed
        elif angle < 180:
            self.x_speed, self.y_speed = self._get_direction(angle - 90, speed)
            self.x_speed, self.y_speed = -self.y_speed, self.x_speed
        elif angle == 180:
            self.x_speed = -speed
            self.y_speed = 0
        elif angle < 270:
            self.x_speed, self.y_speed = self._get_direction(angle - 180, speed)
            self.x_speed, self.y_speed = -self.x_speed, -self.y_speed
        elif angle == 270:
            self.x_speed = 0
            self.y_speed = -speed
        elif angle < 360:
            self.x_speed, self.y_speed = self._get_direction(angle - 270, speed)
            self.x_speed, self.y_speed = self.y_speed, -self.x_speed"""

    @staticmethod
    def _get_direction(angle: int, speed: int):
        """
        Calculates X and Y speed components for a given angle and speed.

        Args:
            angle (int): The angle in degrees.
            speed (int): The speed value.

        Returns:
            tuple: (x_speed, y_speed) as integers.
        """
        # Use Trigonometry to calculate x_speed and y_speed values
        new_x_speed = math.cos(math.radians(angle)) * speed
        new_y_speed = math.sin(math.radians(angle)) * speed

        return round(new_x_speed), round(new_y_speed)

    def get_direction_coordinates(self, angle: int, speed: int) -> Tuple[int, int]:
        """
        Returns the X and Y coordinates for a given angle and speed.

        Args:
            angle (int): The angle in degrees.
            speed (int): The speed value.

        Returns:
            Tuple[int, int]: The X and Y coordinates.
        """
        x, y = 0, 0
        angle += 90
        if angle >= 360:
            angle = angle - 360

        if angle == 0:
            x = speed
            y = 0
        elif angle < 90:
            x, y = self._get_direction(angle + 90, speed)
            x, y = y, x
        elif angle == 90:
            x = 0
            y = -speed
        elif angle < 180:
            x, y = self._get_direction(angle, speed)
            y *= -1
        elif angle == 180:
            x = -speed
            y = 0
        elif angle < 270:
            x, y = self._get_direction(angle - 90, speed)
            y, x = -x, -y
        elif angle == 270:
            x = 0
            y = speed
        elif angle < 360:
            x, y = self._get_direction(angle - 180, speed)
            y, x = y, -x

        return x, y

    def rotate(self, angle: int):
        """
        Rotates the object's image by the given angle.

        Args:
            angle (int): The angle to rotate by (in degrees).
        """

        """if self.curr_rotation > 360:
            self.curr_rotation = self.curr_rotation - 360
        elif self.curr_rotation < 0:
            self.curr_rotation = 350 - self.curr_rotation"""

        self.curr_rotation = self.angle = (angle + self.curr_rotation) % 360

        self.image = pygame.transform.rotate(self.image_orig, self.angle)

        x, y = self.rect.center

        self.rect = self.image.get_rect()

        self.x = x - int((self.rect.width / 2))
        self.y = y - int((self.rect.height / 2))

        self.rect.x = self.x
        self.rect.y = self.y

    def rotate_to_coordinate(self, mouse_x: int, mouse_y: int):
        """
        Rotates the object to face a coordinate (e.g., mouse position).

        Args:
            mouse_x (int): The X coordinate to face.
            mouse_y (int): The Y coordinate to face.
        """
        distance_x = self.x + (self.width / 2) - mouse_x
        distance_y = self.y + (self.height / 2) - mouse_y

        angle = math.degrees(math.atan2(distance_x, distance_y))

        self.curr_rotation = 0
        self.rotate(int(angle))

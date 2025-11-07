from GameFrame import RoomObject
import pygame


class Report_button(RoomObject):
    def __init__(self, room, x, y):
        # Call parent init first
        RoomObject.__init__(self, room, x, y)
        
        # Set these AFTER parent init
        self.handle_mouse_events = True
        self.depth = 10
        
        image = self.load_image("report_button.png")
        self.set_image(image, 300, 200)
        
        # Set both rect AND x,y since Level draws using (x, y)
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        
        # Only add to mouse_objects if not already there
        if self not in room.mouse_objects:
            room.mouse_objects.append(self)

    def clicked(self, button_number):
        """Called when the button is clicked"""
        if button_number == 1:  # Left click
            print("Report button was clicked!")
            # Add your actual button action here

import random

import arcade
from arcade import load_texture

from assets import textures
from assets import names
COM_WIDTH = 75

class Com(arcade.Sprite):
    """
    GUI class to draw the computer players
    Unique names and icons are assigned to each
    """
    def __init__(self, x, y, color, player):
        super().__init__(hit_box_algorithm="None")

        self.center_x = x
        self.center_y = y
        self.value_color = tuple(color)
        self.name = "Com"
        self.player = player
        self.box_size = 150

        # Assign random texture to com
        self.texture = textures.get_random_icon()

    # Highlight com to show hand

    # Set different icons for each com
    @staticmethod
    def assign_unique_icons(com_list):
        available = textures.ICON_TEXTURES.copy()
        random.shuffle(available)
        for com in com_list:
            com.texture = load_texture(available.pop())

    @staticmethod
    def assign_unique_names(com_list):
        available = names.NAMES.copy()
        random.shuffle(available)
        for com in com_list:
            com.name = available.pop()

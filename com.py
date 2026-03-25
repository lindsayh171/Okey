import arcade
from assets import textures
COM_WIDTH = 75

class Com(arcade.Sprite):
    def __init__(self, x, y, color, name, player):
        super().__init__(hit_box_algorithm="None")

        self.center_x = x
        self.center_y = y
        self.value_color = tuple(color)
        self.name = name
        self.player = player
        self.box_size = 150

        # self.texture = arcade.make_soft_square_texture(
        #     self.box_size,
        #     self.value_color,
        #     outer_alpha = 255
        # )

        # Assign random texture to com
        self.texture = textures.get_random_icon()

    # Highlight com to show hand
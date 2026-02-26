import arcade

TILE_WIDTH = 60
TILE_HEIGHT = 100

class Tile(arcade.Sprite):
    def __init__(self, x, y, color, value):
        super().__init__(hit_box_algorithm="None")

        self.value_color = tuple(color)
        self.value = value

        self.texture = arcade.make_soft_square_texture(
            80,
            arcade.color.ANTI_FLASH_WHITE,
            outer_alpha = 255
        )

        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT

        self.center_x = x
        self.center_y = y



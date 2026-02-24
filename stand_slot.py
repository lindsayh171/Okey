import arcade

STAND_WIDTH = 60
STAND_HEIGHT = 75


class Stand_Slot(arcade.Sprite):
    def __init__(self, x, y, color):
        super().__init__(hit_box_algorithm="None")

        self.value_color = tuple(color)

        self.texture = arcade.make_soft_square_texture(
            80,
            self.value_color,
            outer_alpha = 255
        )

        self.width = STAND_WIDTH
        self.height = STAND_HEIGHT

        self.center_x = x
        self.center_y = y



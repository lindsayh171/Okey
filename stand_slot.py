import arcade
from engine.tile import TILE_WIDTH, TILE_HEIGHT

class Stand_Slot:
    def __init__(self, x, y, color):
        self.center_x = x
        self.center_y = y
        self.color = color
        self.size = 5
        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT
        self.border_width = 4

        # For when adding tiles to stand
        self.holding_tile = False

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.center_x - TILE_WIDTH / 2,
            self.center_y - TILE_HEIGHT / 2,
            self.width,
            self.height,
            self.color
        )





import arcade
from engine.tile import TILE_WIDTH, TILE_HEIGHT

DIVIDER_GAP = 5

class StandSlot(arcade.Sprite):
    """
    Slots for each spot in the stand
    """
    def __init__(self, x, y, color):
        super().__init__()

        self.center_x = x
        self.center_y = y
        self.color = color
        self.scale = 5
        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT
        self.border_width = 4

        # For when adding tiles to stand
        self.curr_tile = None
        self.holding_tile = False

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.center_x - TILE_WIDTH / 2,
            self.center_y - TILE_HEIGHT / 2,
            self.width,
            self.height,
            self.color
        )

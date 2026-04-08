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
        self.border_width = 4

        # For when adding tiles to stand
        self.holding_tile = False
        # Set on OpenStand slots so drops go into the right open_tiles[row]
        self.open_row_index = None
        # OpenStand only: "before" = prepend, "after" = append; occupied slots stay None
        self.open_edge = None

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.center_x - TILE_WIDTH / 2,
            self.center_y - TILE_HEIGHT / 2,
            TILE_WIDTH,
            TILE_HEIGHT,
            self.color
        )

    def tile_overlaps(self, tile):
        return (
            # make sure tile is less than a tile away from slot
            abs(tile.center_x - self.center_x) * 2 < TILE_WIDTH
            and abs(tile.center_y - self.center_y) * 2 < TILE_HEIGHT
        )

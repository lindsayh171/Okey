import arcade
from engine.tile import TILE_WIDTH, TILE_HEIGHT

class DiscardPile(arcade.Sprite):
    """
    Pile of tiles that a player has discarded
    """

    BORDER_WIDTH = 4

    def __init__(self, x, y, tiles=None):
        super().__init__(hit_box_algorithm="None")

        # list of tiles that are in this discard pile
        if tiles is None:
            self.tiles = []
        else:
            self.tiles = tiles

        self.center_x = x
        self.center_y = y
        self.held_tiles = []
        self.player_discard = False
        self.player_com_discard = False
        self.holding_tile = False

    def count(self):
        return len(self.tiles)

    def draw_tile(self):
        if len(self.tiles) > 0:
            return self.tiles.pop()
        return None

    def draw(self):
        arcade.draw_lbwh_rectangle_outline(
            self.center_x - TILE_WIDTH / 2,
            self.center_y - TILE_HEIGHT / 2,
            TILE_WIDTH + self.BORDER_WIDTH,
            TILE_HEIGHT + self.BORDER_WIDTH,
            arcade.color.DEEP_COFFEE,
            self.BORDER_WIDTH
        )

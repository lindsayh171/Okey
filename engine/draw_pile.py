import arcade
import ui_components.rounded_rectangle as rr
import assets.colors as colr
from engine.tile import TILE_WIDTH, TILE_HEIGHT

STACK_LAYERS = 5

class DrawPile(arcade.Sprite):
    """
    Pile of cards left to draw_tile
    """
    def __init__(self, x, y, tiles=None):
        super().__init__(hit_box_algorithm="None")

        # avoids multiple objects from sharing same list in memory
        if tiles is None:
            self.tiles = []
        else:
            self.tiles = tiles

        self.center_x = x
        self.center_y = y

        self.label_x = self.center_x + TILE_WIDTH / 2
        self.label_y = self.center_y + TILE_HEIGHT / 2
        self.tile_count_text = arcade.Text(
            str(self.count()),
            self.label_x,
            self.label_y,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
            anchor_y="center",
        )

        self.draw_highlight = False
        self.highlight_tile = rr.RoundedRectangle(
                [self.center_x, self.center_y],
                [TILE_WIDTH + 10, TILE_HEIGHT + 10],
                TILE_HEIGHT // 9,
                colr.LIGHT_GOLDENROD_YELLOW,
            )
        self.back_tile = rr.RoundedRectangle(
            [self.center_x, self.center_y],
            [TILE_WIDTH, TILE_HEIGHT],
            TILE_HEIGHT // 9,
            (222, 212, 193)
        )

    def count(self):
        return len(self.tiles)

    def draw_tile(self):
        if len(self.tiles) == 0:
            raise ValueError("DrawPile.draw_tile() called without tiles")
        # for every call, one tile is drawn out
        return self.tiles.pop()

    def draw(self):


        if self.draw_highlight:
            self.highlight_tile.draw()

        # Back of top tile

        self.back_tile.draw()

        # label
        arcade.draw_circle_filled(self.label_x,
                                 self.label_y,
                                 TILE_WIDTH/4,
                                 colr.THEME_DARK_BLUE,
                                 num_segments=-1)
        self.tile_count_text.text = self.count()
        self.tile_count_text.draw()

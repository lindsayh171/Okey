import arcade
import ui_components.rounded_rectangle as rr
import assets.colors as colr
from engine.tile import TILE_WIDTH, TILE_HEIGHT

STACK_LAYERS = 5

class GuiDrawPile(arcade.Sprite):
    """
    Keeps track of all the tiles in the deck
    """
    def __init__(self, x, y, draw_pile):
        super().__init__(hit_box_algorithm="None")

        self.center_x = x
        self.center_y = y
        self.draw_pile = draw_pile

        # create label
        tile_count = self.draw_pile.count()
        self.label_x = self.center_x + TILE_WIDTH/2
        self.label_y = self.center_y + TILE_HEIGHT/2
        self.tile_count_text = arcade.Text(
            str(tile_count),
            self.label_x,
            self.label_y,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
            anchor_y="center",
        )

    def draw(self):
        # Back of top tile

        back_tile = rr.RoundedRectangle(
            self.center_x,
            self.center_y,
            TILE_WIDTH,
            TILE_HEIGHT,
            TILE_HEIGHT // 9,
            (222, 212, 193)
        )
        back_tile.draw()

        # label
        arcade.draw_circle_filled(self.label_x,
                                 self.label_y,
                                 TILE_WIDTH/4,
                                 colr.THEME_DARK_BLUE,
                                 num_segments=-1)

        self.tile_count_text.draw()

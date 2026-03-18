import arcade
import ui_components.rounded_rectangle as rr

from engine.draw_pile import DrawPile
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

    def draw(self):
        tile_count = self.draw_pile.count()

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

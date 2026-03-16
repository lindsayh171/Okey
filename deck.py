import arcade

from engine.tile import TILE_WIDTH, TILE_HEIGHT

class Deck:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y

        # For when there are tiles to put in the deck
        #self.tiles = arcade.SpriteList()

    def draw(self):
        arcade.draw_lbwh_rectangle_outline(
            self.center_x - TILE_WIDTH / 2,
            self.center_y - TILE_HEIGHT / 2,
            TILE_WIDTH,
            TILE_HEIGHT,
            arcade.color.ASH_GREY,
            4
        )

        # Draw tiles on top

        # Add tile function

        # Draw tile function


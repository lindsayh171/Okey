import arcade
from Sprites.tile import Tile, TILE_WIDTH, TILE_HEIGHT

# Game window class
class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(
            800,
            600,
            "Test Game",
            resizable=True
        )
        self.background_color = arcade.color.FOREST_GREEN

        # List of tiles no matter where they are in game
        self.tile_list = arcade.SpriteList()

    # Set up game
    def setup(self):

        # TODO: maybe separate this out into another file
        x = 0
        y = 300
        for i in range(1, 14):
            # red tile
            tile = Tile(x, y, arcade.color.RED, i)
            self.tile_list.append(tile)
            x+=TILE_WIDTH + 2

            # orange tile
            tile = Tile(x, y, arcade.color.ORANGE, i)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2

            # blue tile
            tile = Tile(x, y, arcade.color.BLUE, i)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2

            # black tile
            tile = Tile(x, y, arcade.color.BLACK, i)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2

        for i in range(1, 3):
            tile = Tile(x, y, arcade.color.GREEN, "★")
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2



    # Screen render that clears the board
    def on_draw(self):
        self.clear()

        self.tile_list.draw()

        for tile in self.tile_list:
            # Rectangle
            arcade.draw_lbwh_rectangle_filled(
                tile.center_x - TILE_WIDTH / 2,
                tile.center_y - TILE_HEIGHT / 2,
                TILE_WIDTH,
                TILE_HEIGHT,
                (222, 212, 193)
            )

            # Value
            arcade.draw_text(
                str(tile.value),
                tile.center_x,
                tile.center_y + (TILE_HEIGHT / 5),
                tile.value_color,
                40,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            # Symbol
            arcade.draw_text(
                "♥",
                tile.center_x,
                tile.center_y - (TILE_HEIGHT / 3.5),
                tile.value_color,
                15,
                anchor_x="center",
                anchor_y="center"
            )

    # When user presses a mouse button
    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    # When user releases a mouse button
    def on_mouse_release(self, x, y, button, key_modifiers):
        pass

    # When user moves the mouse
    def on_mouse_motion(self, x, y, dx, dy):
        pass

def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()


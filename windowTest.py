import arcade
from tile import Tile, TILE_WIDTH, TILE_HEIGHT
from stand_slot import Stand_Slot, STAND_WIDTH, STAND_HEIGHT

# Game window class
class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(
            800,
            600,
            "Test Game",
            resizable=True
        )
        self.background_color = arcade.color.LINCOLN_GREEN

        self.stand_slot_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()

        self.stand_start_x = 0
        self.stand_start_y = 0
        self.rows = 2
        self.columns = 12
        self.total_stand_width = self.columns * STAND_WIDTH



    # Set up game
    def setup(self):
        self.stand_slot_list.clear()

        # Width of the whole screen
        screen_width = self.width

        # Where to start the stand based on the size of the screen
        self.stand_start_x = (screen_width - self.total_stand_width) / 2 + STAND_WIDTH / 2
        self.stand_start_y = STAND_HEIGHT + 20

        # 2 rows in the tile stand
        for row in range(self.rows):
            # 12 slots on each row
            for column in range(self.columns):
                # stand_slot position
                stand_x = self.stand_start_x + (column * STAND_WIDTH)
                stand_y = self.stand_start_y - row * STAND_HEIGHT

                # create stand_slot and append to the slot list
                stand_slot = Stand_Slot(stand_x, stand_y, arcade.color.BEAVER)
                self.stand_slot_list.append(stand_slot)



    # Screen render that clears the board
    def on_draw(self):
        self.clear()

        self.stand_slot_list.draw()

        # Stand line divider
        divider_y = self.stand_start_y - (STAND_HEIGHT / 2)

        # Com icon boxes

        # Deck outline

        # Discard pile outlines


def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()


import arcade
from com import Com, COM_WIDTH
from deck import Deck
from engine.tile import Tile, TILE_WIDTH, TILE_HEIGHT, TILE_COLORS_SYMBOLS
from stand_slot import Stand_Slot
from discard import Discard

# Game window class
class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(
            1000,
            800,
            "Test Game",
            resizable=True
        )
        self.background_color = arcade.color.LINCOLN_GREEN

        # Sprite list goes here
        self.tile_list = arcade.SpriteList()
        self.com_list = arcade.SpriteList()

        # Non-sprite lists
        self.discard_list = []
        self.stand_slot_list = []

        # Stand specifications
        self.stand_start_x = 0
        self.stand_divider = 5
        self.rows = 2
        self.columns = 12
        self.total_stand_height = self.rows * TILE_HEIGHT + self.stand_divider
        self.total_stand_width = self.columns * TILE_WIDTH

        self.held_tiles = []

    # Set up game
    def setup(self):

        # Clear any existing sprites
        self.stand_slot_list.clear()
        self.tile_list.clear()
        self.com_list.clear()
        self.discard_list.clear()
        # Stand coordinates
        self.setup_stand()
        # Com coordinates
        self.setup_coms()
        # Deck coordinates
        self.setup_deck()
        # Discard pile coordinates
        self.setup_discard()

        # TODO: maybe separate this out into another file
        # create tiles
        x = 0
        y = 300
        for i in range(1, 14):
            for color in TILE_COLORS_SYMBOLS.keys():
                tile = Tile(x, y, i, color, TILE_COLORS_SYMBOLS[color])
                self.tile_list.append(tile)
                x += TILE_WIDTH + 2

                tile = Tile(x, y, i, color, TILE_COLORS_SYMBOLS[color])
                self.tile_list.append(tile)
                x += TILE_WIDTH + 2

        # create jokers
        for i in range(1, 3):
            tile = Tile(x, y, "〠", arcade.color.FOREST_GREEN, "⚡", True)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2



    # Screen render that clears the board
    def on_draw(self):
        self.clear()

        self.tile_list.draw()

        # Draw stand
        for stand in self.stand_slot_list:
            stand.draw()

        # draw stand line divider
        arcade.draw_lbwh_rectangle_filled(
            self.stand_start_x - TILE_WIDTH / 2,
            TILE_HEIGHT,
            self.total_stand_width,
            self.stand_divider,
            arcade.color.DEEP_COFFEE,
        )

        # Draw coms
        self.com_list.draw()
        for com in self.com_list:
            # Need to add text to existing sprite square texture
            arcade.draw_text(
                com.name,
                com.center_x,
                com.center_y,
                arcade.color.WHITE,
                font_size=15,
                anchor_x="center",
                anchor_y="center",
            )

        # Draw discard piles
        for disc in self.discard_list:
            disc.draw()
        # Draw deck
        self.deck.draw()

        for tile in self.tile_list:
            tile.set_face_up()
            # Rectangle
            tile.draw()

    def setup_stand(self):
        screen_width = self.width

        # Coordinates of the stand based on the size of the screen
        self.stand_start_x = (screen_width - self.total_stand_width) / 2 + TILE_WIDTH / 2

        # 2 rows in the tile stand
        for row in range(self.rows):
            stand_y = (TILE_HEIGHT / 2) + row * TILE_HEIGHT
            # 12 slots on each row
            for column in range(self.columns):
                # stand_slot position
                stand_x = self.stand_start_x + column * TILE_WIDTH

                # create stand_slot and append to the slot list
                stand_slot = Stand_Slot(stand_x, stand_y, arcade.color.BEAVER)
                self.stand_slot_list.append(stand_slot)

    # Com setup
    def setup_coms(self):
        screen_width = self.width
        screen_height = self.height

        # Com coordinates
        com1_x = COM_WIDTH
        com1_y = screen_height / 2
        com2_x = self.width / 2
        com2_y = screen_height - COM_WIDTH
        com3_x = screen_width - COM_WIDTH
        com3_y = screen_height / 2

        # Make each com
        com1 = Com(com1_x, com1_y, arcade.color.RED, "Com 1")
        com2 = Com(com2_x, com2_y, arcade.color.YELLOW, "Com 2")
        com3 = Com(com3_x, com3_y, arcade.color.BLUE, "Com 3")

        # Add each com to the list
        self.com_list.append(com1)
        self.com_list.append(com2)
        self.com_list.append(com3)

    # Discard piles setup
    def setup_discard(self):

        # Placing discards on thirds of the screen size
        third_width = self.width / 3
        third_height = self.height / 3

        # Discard pile coordinates
        left_disc_x = third_width - TILE_WIDTH
        right_disc_x = third_width * 2 + TILE_WIDTH
        top_disc_y = third_height * 2
        bottom_disc_y = third_height

        # Make each discard pile
        com1_disc = Discard(left_disc_x, bottom_disc_y, )
        com2_disc = Discard(right_disc_x, top_disc_y, )
        com3_disc = Discard(left_disc_x, top_disc_y, )
        player_disc = Discard(right_disc_x, bottom_disc_y, )

        # Add discard piles to list
        self.discard_list.append(com1_disc)
        self.discard_list.append(com2_disc)
        self.discard_list.append(com3_disc)
        self.discard_list.append(player_disc)

    # Deck setup
    def setup_deck(self):
        self.deck = Deck(
            self.width / 2,
            self.height / 2,
        )

    # Resize window
    def on_resize(self, width, height):
        super().on_resize(width, height)
        # Run setup again with new screen size
        self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        clicked_tiles = arcade.get_sprites_at_point((x, y), self.tile_list)

        # Check if a card had been clicked
        if len(clicked_tiles) > 0:
            self.held_tiles.append(clicked_tiles[0])
            self.pull_to_top(self.held_tiles[0])

    def on_mouse_release(self, x, y, button, modifiers):

        # If no cards are being held, return
        if len(self.held_tiles) == 0:
            return

        # Drop card from held tiles
        self.held_tiles = []

        # Find closest stand slot



    def on_mouse_motion(self, x, y, dx, dy):
        for moving_tile in self.held_tiles:
            moving_tile.center_x += dx
            moving_tile.center_y += dy

    def pull_to_top(self, selected_tile: arcade.Sprite):
        self.tile_list.remove(selected_tile)
        self.tile_list.append(selected_tile)

def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()


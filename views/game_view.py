import math
import arcade
from com import Com, COM_WIDTH
from deck import Deck
from stand_slot import Stand_Slot
from engine.game import Game
from engine.tile import Tile, TILE_WIDTH, TILE_HEIGHT, TILE_COLORS_SYMBOLS
import assets.colors as colr

# Game window class
class GameView(arcade.View):
    """
    Main view for the program as the game is being played
    """
    def __init__(self):
        super().__init__()

        # create a new game
        self.game = Game(self.width, self.height)

        self.background_color = colr.THEME_LIGHT_BLUE

        # Sprite list goes here
        # TODO: use the hand from human player as the list of tiles
        self.tile_list = arcade.SpriteList()
        self.com_list = arcade.SpriteList()

        # com text
        self.com_labels = []

        # Non-sprite lists
        self.stand_slot_list = []

        # Stand specifications
        self.stand_start_x = 0
        self.stand_divider = 5
        self.rows = 2
        self.columns = 12
        self.total_stand_height = self.rows * TILE_HEIGHT + self.stand_divider
        self.total_stand_width = self.columns * TILE_WIDTH

        self.held_tiles = []
        self.deck = None

    # Set up game
    def setup(self):
        # need to do this here so width and height are set up
        self.game = Game(self.width, self.height)

        # Clear any existing sprites
        self.stand_slot_list.clear()
        self.tile_list.clear()
        self.com_list.clear()

        # Stand coordinates
        self.setup_stand()
        # Com coordinates
        self.setup_coms()
        # Deck coordinates
        self.setup_deck()

        # TODO: maybe separate this out into another file
        # create tiles
        x = 0
        y = 300
        for i in range(1, 14):
            for color, symbol in TILE_COLORS_SYMBOLS.items():
                tile = Tile(x, y, i, color, symbol)
                self.tile_list.append(tile)
                x += TILE_WIDTH + 2

                tile = Tile(x, y, i, color, symbol)
                self.tile_list.append(tile)
                x += TILE_WIDTH + 2

        # create jokers
        for i in range(1, 3):
            tile = Tile(x, y, "〠", arcade.color.FOREST_GREEN, "⚡", True)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2

        # player name pop-up
        self.game.enter_player_name()

        # play the game
        self.game.play_game()

    # Screen render that clears the board
    def on_draw(self):
        self.clear()

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
        for label in self.com_labels:
            label.draw()

        # Draw discard piles
        for disc in self.game.discards:
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

        # create labels
        for com in self.com_list:
            # Need to add text to existing sprite square texture
            label = arcade.Text(
                com.name,
                com.center_x,
                com.center_y,
                arcade.color.WHITE,
                font_size=15,
                anchor_x="center",
                anchor_y="center",
            )
            self.com_labels.append(label)

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

        # Add player discard pile to list of slots
        available_slots = self.stand_slot_list
        for disc in self.game.discards:
            if disc.player_discard:
                available_slots.append(disc)

        # Snap tile to the closest stand slot
        if len(self.held_tiles) > 0:
            self.snap(self.held_tiles[0], self.stand_slot_list)

        # Drop card from held tiles
        self.held_tiles = []

    def on_mouse_motion(self, x, y, dx, dy):
        for moving_tile in self.held_tiles:
            moving_tile.center_x += dx
            moving_tile.center_y += dy

    def pull_to_top(self, selected_tile: arcade.Sprite):
        self.tile_list.remove(selected_tile)
        self.tile_list.append(selected_tile)

    # Snap tile to a slot location
    def snap(self, tile, selected_list):
        current_best = 10000
        best_slot = None
        snap_threshold = 80

        # Loop through all stand slots and find the closest distance to tile
        for slot in selected_list:
            # Using Euclidean distance formula to find the closest stand slot
            difference = math.sqrt((slot.center_x - tile.center_x) ** 2 +
                                   (slot.center_y - tile.center_y) ** 2)

            # Update current best if distance is less than it
            if difference < current_best and slot.holding_tile is not True:
                current_best = difference
                best_slot = slot

        # Only snap if there is a best slot and is within the threshold
        if best_slot is not None and current_best < snap_threshold:
            tile.center_x = best_slot.center_x
            tile.center_y = best_slot.center_y
            best_slot.holding_tile = True
            # Check if tile was located at another slot previously
            if tile.current_slot_location is not None:
                # Get previous slot location and set holding tile to false since the tile is moving
                previous_slot = tile.current_slot_location
                previous_slot.holding_tile = False

            tile.current_slot_location = best_slot

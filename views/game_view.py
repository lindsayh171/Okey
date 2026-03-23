import math
import arcade
from com import Com, COM_WIDTH
from gui_draw_pile import GuiDrawPile
from stand_slot import StandSlot, DIVIDER_GAP
from engine.game import Game
from engine.tile import TILE_WIDTH, TILE_HEIGHT
import assets.colors as colr
import ui_components.button as ui_button

# Game window class
class GameView(arcade.View):
    """
    Main view for the program as the game is being played
    """
    def __init__(self):
        super().__init__()

        # create a new game
        self.game = None

        self.background_color = colr.THEME_LIGHT_BLUE

        # Sprite list goes here
        self.com_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()

        # com text
        self.com_labels = []
        self.com_displaying_hand = False

        # Non-sprite lists
        self.stand_slot_list = []
        self.com_stand_slot_list = []

        # Stand specifications
        self.stand_start_x = 0
        self.com_stand_start_x = 0
        self.stand_divider = 5
        self.rows = 2
        self.columns = 12
        self.total_stand_height = self.rows * TILE_HEIGHT + self.stand_divider
        self.total_stand_width = self.columns * TILE_WIDTH

        self.held_tiles = []
        self.draw_pile = None
        self.draw_pile_label = None

        self.player_discard = None

        self.player_hand = None

        # menu
        self.menu_button = ui_button.Button(self.window.width * 0.9,
                                         self.window.height * 0.9,
                                         self.window.width / 15,
                                         self.window.width / 15,
                                         "☰",
                                         colr.THEME_LIGHT_BLUE,
                                         colr.THEME_DARK_BLUE)

        self.com_stand_button = None

    # Set up game
    def setup(self):
        # need to do this here so width and height are set up
        self.game = Game(self.width, self.height)
        self.game.start_game()


        # Clear any existing sprites
        self.stand_slot_list.clear()
        self.tile_list.clear()
        self.com_list.clear()

        # Stand coordinates
        self.setup_stand()
        # Com coordinates
        self.setup_coms()
        # Draw pile coordinates
        self.setup_draw_pile()

        self.setup_player_tiles()
        # Com hand display tracker
        self.com_displaying_hand = None

        # player name pop-up
        # self.game.enter_player_name()

    def on_show_view(self):
        self.background_color = colr.THEME_LIGHT_BLUE

    # Screen render that clears the board
    def on_draw(self):
        self.clear()

        # Draw stand slots
        for stand in self.stand_slot_list:
            stand.draw()

        # draw stand line divider
        arcade.draw_lbwh_rectangle_filled(
            self.stand_start_x - TILE_WIDTH / 2,
            (TILE_HEIGHT + DIVIDER_GAP / 2) - self.stand_divider / 2,
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

        # Draw draw pile
        self.draw_pile.draw()
        # Update text to show count of deck
        self.draw_pile_label.text = str(self.game.draw_pile.count())
        self.draw_pile_label.draw()

        if self.com_displaying_hand is not None:
            # Draw window box
            arcade.draw_lbwh_rectangle_filled(
                2 * COM_WIDTH + DIVIDER_GAP,
                self.total_stand_height + DIVIDER_GAP,
                self.width - (4 * COM_WIDTH + 2 * DIVIDER_GAP),
                self.height - self.total_stand_height - 2 * COM_WIDTH - 2 * DIVIDER_GAP,
                arcade.color.GRAY_BLUE
            )

            # Draw slots
            for slot in self.com_stand_slot_list:
                slot.draw()

            # Draw X button
            self.com_stand_button.draw()

        self.menu_button.draw()

        # Draw tiles at end on top of everything.
        for tile in self.tile_list:
            tile.draw()

    def setup_stand(self):
        screen_width = self.width

        # Coordinates of the stand based on the size of the screen
        self.stand_start_x = (screen_width - self.total_stand_width) / 2 + TILE_WIDTH / 2

        # 2 rows in the tile stand
        for row in range(self.rows):
            stand_y = (TILE_HEIGHT / 2) + row * (TILE_HEIGHT + DIVIDER_GAP)
            # 12 slots on each row
            for column in range(self.columns):
                # stand_slot position
                stand_x = self.stand_start_x + column * TILE_WIDTH

                # create stand_slot and append to the slot list
                stand_slot = StandSlot(stand_x, stand_y, arcade.color.BEAVER)
                self.stand_slot_list.append(stand_slot)

    def setup_player_tiles(self):
        for i, tile in enumerate(self.game.players[0].hand):
            tile.set_curr_slot(self.stand_slot_list[i])
            self.stand_slot_list[i].holding_tile = True
            tile.set_face_up()
            self.tile_list.append(tile)

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
        com1 = Com(com1_x, com1_y, arcade.color.RED, "Com 1", self.game.players[1])
        com2 = Com(com2_x, com2_y, arcade.color.YELLOW, "Com 2", self.game.players[2])
        com3 = Com(com3_x, com3_y, arcade.color.BLUE, "Com 3", self.game.players[3])

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

    # Draw pile setup
    def setup_draw_pile(self):
        self.draw_pile = GuiDrawPile(
            self.width / 2,
            self.height / 2,
            self.game.draw_pile,
        )
        self.draw_pile_label = arcade.Text(
            # Show how many tiles are in the deck
            str(self.game.draw_pile.count()),
            self.width / 2,
            self.height / 2,
            arcade.color.EGGSHELL,
            16,
            anchor_x="center",
            anchor_y="center",
        )

    # Discard setup
    def setup_discard(self, player):
        pass

    # Resize window
    def on_resize(self, width, height):
        super().on_resize(width, height)
        # Run setup again with new screen size
        self.setup()

    def on_mouse_press(self, x, y, button, modifiers):

        # TILE IS CLICKED
        clicked_tiles = arcade.get_sprites_at_point((x, y), self.tile_list)
        if len(clicked_tiles) > 0:
            self.held_tiles.append(clicked_tiles[0])
            self.pull_to_top(self.held_tiles[0])
            if clicked_tiles[0] in self.held_tiles:
                clicked_tiles[0].current_slot.holding_tile = False
            # Return if clicked
            return

        if self.com_displaying_hand is None:
            # Check if a card had been clicked
            if len(clicked_tiles) > 0:
                self.held_tiles.append(clicked_tiles[0])
                self.pull_to_top(self.held_tiles[0])
                # Return if clicked
                return

            # Check if draw pile was clicked
            if self.draw_pile.collides_with_point((x, y)):
                # Initial check if player has drawn already this round
                if self.game.players[0].drawn:
                    return

                # Draw top tile from draw pile
                if self.game.draw_pile.count() > 0:
                    # Add tile to players logic hand
                    print("drawn from draw pile")
                    self.game.players[0].drawn = True

                    top_tile = self.game.draw_pile.draw()
                    self.game.players[0].draw_tile(top_tile)

                # Add tile to gui hand
                for slot in self.stand_slot_list:
                    if not slot.holding_tile:
                        top_tile.center_x = slot.center_x
                        top_tile.center_y = slot.center_y
                        slot.holding_tile = True
                        top_tile.current_slot_location = slot
                        top_tile.set_face_up()
                        self.tile_list.append(top_tile)
                        break

            # Check if discard player accesses was clicked
            for discard in self.game.discards:
                # Check if clicked on discard not for player to access
                if discard.collides_with_point((x, y)):
                    if not discard.player_com_discard:
                        continue
                    print("drawn from discard pile")

                    # Check if player has already drawn
                    if self.game.players[0].drawn:
                        return

                    if discard.count() > 0:
                        print("drawn from discard pile")
                        self.game.players[0].drawn = True

                        top_tile = discard.draw_tile()
                        self.game.players[0].draw_tile(top_tile)

                        # Add tile to gui hand
                        for slot in self.stand_slot_list:
                            if not slot.holding_tile:
                                top_tile.center_x = slot.center_x
                                top_tile.center_y = slot.center_y
                                slot.holding_tile = True
                                top_tile.current_slot_location = slot
                                break
                        self.tile_list.append(top_tile)
                        return

        # Check if clicked on com
        for com in self.com_list:
            # TODO: Once a boolean for player being open, add and statement to check
            if com.collides_with_point((x, y)):

                # No coms are displaying their hand
                if self.com_displaying_hand is None:
                    # Display hand
                    self.com_displaying_hand = com
                    # TODO: Delete this line once we have logic implemented
                    com.player.sets_played = [[1,2,3,4], [4, 4, 4], [9, 10, 11, 12], [1, 1, 1, 1, 1]]
                    self.setup_com_stand(com)
                    return

                # If a com that isn't the current displaying hand is clicked
                if com is not self.com_displaying_hand or self.com_displaying_hand:
                    continue

        # Turn hand display off if pressed x button
        if self.com_displaying_hand is not None and self.com_stand_button is not None:
            if self.com_stand_button.button_pressed(x,y):
                # Delete saved display hand
                self.com_stand_slot_list.clear()
                self.com_displaying_hand = None
                return


        # check if menu was clicked
        if self.menu_button.button_pressed(x, y):
            from views.menu_view import MenuView

            self.window.show_view(MenuView(self))

    def on_mouse_release(self, x, y, button, modifiers):

        # If no cards are being held, return
        if len(self.held_tiles) == 0:
            return

        # Add player discard pile to list of slots
        available_slots = list(self.stand_slot_list)
        for disc in self.game.discards:
            if disc.player_discard:
                available_slots.append(disc)

        # Snap tile to the closest stand slot or a com hand if displayed
        if len(self.held_tiles) > 0:
            # TODO: Allow snapping to player hand and com hands only if com hand is displayed
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
        snap_threshold = 80  # You might adjust this if needed

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

    def setup_com_stand(self, com):
        self.com_stand_slot_list.clear()

        # Coordinates of the stand based on the size of the screen
        self.com_stand_start_x = 2 * COM_WIDTH + DIVIDER_GAP + TILE_WIDTH / 2

        start_y = self.total_stand_height + TILE_HEIGHT / 2 + DIVIDER_GAP

        button_size = 30
        self.com_stand_button = ui_button.Button(
            2 * COM_WIDTH + DIVIDER_GAP + button_size / 2,
            self.height - (self.total_stand_height - COM_WIDTH) - DIVIDER_GAP,
            button_size,
            button_size,
            "X",
            arcade.color.RED,
            arcade.color.BLACK
        )

        # Build as many rows as the player has sets in their open
        for current_set in range(len(com.player.sets_played)):
            stand_y = start_y + current_set * (TILE_HEIGHT + 2 * DIVIDER_GAP)
            # Build as many columns as there are length of the current set + 2 empty slots on either side
            for column in range(len(com.player.sets_played[current_set]) + 4):
                # stand_slot position
                stand_x = self.com_stand_start_x + column * TILE_WIDTH

                # create stand_slot and append to the slot list
                stand_slot = StandSlot(stand_x, stand_y, arcade.color.GRAY_BLUE)
                self.com_stand_slot_list.append(stand_slot)

        # Insert tiles onto stand
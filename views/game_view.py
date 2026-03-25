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
        self.open_stand_start_x = 0
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

        self.open_displaying_player = None
        self.open_stand_slot_list = []
        self.current_open_tiles = []
        self.open_window_tiles = []

        # menu
        self.menu_button = ui_button.Button(self.window.width * 0.9,
                                         self.window.height * 0.9,
                                         self.window.width / 15,
                                         self.window.width / 15,
                                         "☰",
                                         colr.THEME_LIGHT_BLUE,
                                         colr.THEME_DARK_BLUE)

        # open button

        # open button
        self.open_button = ui_button.Button(self.window.width * 0.07,
                                            self.window.height * 0.07,
                                            self.window.width / 6,
                                            self.window.width / 13,
                                            "Open",
                                            colr.THEME_PINK,
                                            colr.THEME_LIGHT_BLUE)

    # Set up game
    def setup(self):
        # need to do this here so width and height are set up
        self.game = Game(self.width, self.height)
        self.game.start_game()


        # TODO: DELETE THESE TWO LINES, ONLY HERE FOR TESTING PLAYER OPEN
        self.game.players[0].can_open = True
        self.game.players[0].sets_played = [[1, 2, 3, 4], [4, 4, 4], [9, 10, 11, 12],
                                            [1, 1, 1, 1, 1]]


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

        if self.open_displaying_player is not None:
            # Draw window box
            arcade.draw_lbwh_rectangle_filled(
                2 * COM_WIDTH + DIVIDER_GAP,
                self.total_stand_height + DIVIDER_GAP,
                self.width - (4 * COM_WIDTH + 2 * DIVIDER_GAP),
                self.height - self.total_stand_height - 2 * COM_WIDTH - 2 * DIVIDER_GAP,
                arcade.color.GRAY_BLUE
            )

            # Draw slots
            for slot in self.open_stand_slot_list:
                slot.draw()


        self.menu_button.draw()
        self.open_button.draw()

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
                com.center_y - COM_WIDTH - 15, # minus 15 for font size
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
            # Return if clicked
            return

        if self.open_displaying_player is None:
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
                        top_tile.current_slot = slot
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
                                top_tile.current_slot = slot
                                break
                        self.tile_list.append(top_tile)
                        return

        # Check if clicked on com
        for com in self.com_list:
            # TODO: Once a boolean for player being open, add and statement to check
            if com.collides_with_point((x, y)):

                # No coms are displaying their hand
                if self.open_displaying_player is None:
                    # Display hand
                    self.open_displaying_player = com.player
                    # TODO: Delete this line once we have logic implemented
                    com.player.sets_played = [[1,2,3,4], [4, 4, 4], [9, 10, 11, 12],
                                              [1, 1, 1, 1, 1]]
                    self.setup_open_stand(com.player)
                    return

                # Closing currently open com window
                if self.open_displaying_player == com.player:
                    # Remove tile display with window
                    for tile in self.open_window_tiles:
                        if tile in self.tile_list:
                            self.tile_list.remove(tile)
                            tile.current_slot = None
                        else:
                            continue
                    self.open_window_tiles.clear()
                    self.open_stand_slot_list.clear()
                    self.open_displaying_player = None
                    return

        # Check if open button was clicked
        if self.open_button.button_pressed(x, y) and self.game.players[0].can_open:
            # See if any open window is displaying
            if self.open_displaying_player is None:
                self.open_displaying_player = self.game.players[0]
                self.setup_open_stand(self.open_displaying_player)
            # Stop displaying player open window
            else:
                # Save tile to open sets list
                if self.current_open_tiles:
                    self.open_displaying_player.sets_played.append(self.current_open_tiles.copy())
                # Remove tile display with window
                for tile in self.open_window_tiles:
                    if tile in self.tile_list:
                        self.tile_list.remove(tile)
                        tile.current_slot = None
                    else:
                        continue
                self.open_window_tiles.clear()
                self.current_open_tiles.clear()
                self.open_stand_slot_list.clear()
                self.open_displaying_player = None
            return

        # check if menu was clicked
        if self.menu_button.button_pressed(x, y):
            from views.menu_view import MenuView

            self.window.show_view(MenuView(self))

    def on_mouse_release(self, x, y, button, modifiers):
        # If no cards are being held, return
        if len(self.held_tiles) == 0:
            return

        tile = self.held_tiles[0]

        # Put tile in discard pile
        available_slots = list(self.stand_slot_list)
        disc = self.game.discards[0]
        if arcade.check_for_collision(tile, disc):
            # TODO: prevent someone from picking this back up
            tile.position = (disc.center_x, disc.center_y)
            self.held_tiles = []
            return

        # Snap tile to the closest stand slot or a com hand if displayed
        if len(self.held_tiles) > 0:
            # snapping to another open set
            if self.open_displaying_player is not None:
                # Combine player stand slots and window slots
                combined_slots = self.stand_slot_list + self.open_stand_slot_list
                self.snap(tile, combined_slots)
                # TODO: check if placing tile matches with set
                if tile.current_slot in self.open_stand_slot_list:
                    self.current_open_tiles.append(tile)
                    self.open_window_tiles.append(tile)
            else:
                self.snap(self.held_tiles[0], available_slots)

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
        reset_position = True

        # find the closest spot by looping through list
        available_slots = list(selected_list)
        slot, _ = arcade.get_closest_sprite(tile, available_slots)

        while available_slots and reset_position:
            # if closest slot is empty and tile is on top of it at all, snap
            if not slot.holding_tile and arcade.check_for_collision(tile, slot):
                tile.position = slot.center_x, slot.center_y
                slot.holding_tile = True

                # reset previous slot before changing curr slot to new location
                tile.current_slot.holding_tile = False
                tile.current_slot = slot
                reset_position = False
            else:
                # try another slot
                available_slots.remove(slot)
                result = arcade.get_closest_sprite(tile, available_slots)

                # check for empty response
                if result is None:
                    break
                slot, _ = result

        # if invalid spot reset
        if reset_position:
            tile.position = tile.current_slot.center_x, tile.current_slot.center_y

    def setup_open_stand(self, player):
        self.open_stand_slot_list.clear()
        self.current_open_tiles.clear()

        # Coordinates of the stand based on the size of the screen
        self.open_stand_start_x = 2 * COM_WIDTH + DIVIDER_GAP + TILE_WIDTH / 2

        start_y = self.total_stand_height + TILE_HEIGHT / 2 + DIVIDER_GAP

        # Build as many rows as the player has sets in their open
        for current_set, played_set in enumerate(player.sets_played):
            stand_y = start_y + current_set * (TILE_HEIGHT + 2 * DIVIDER_GAP)
            # Build as many columns as there are length of the current set +
            # 2 empty slots on either side
            for column in range(len(player.sets_played[current_set]) + 4):
                # stand_slot position
                stand_x = self.open_stand_start_x + column * TILE_WIDTH

                # create stand_slot and append to the slot list
                stand_slot = StandSlot(stand_x, stand_y, arcade.color.BLUE)
                stand_slot.holding_tile = False
                self.open_stand_slot_list.append(stand_slot)

        # Insert tiles onto stand

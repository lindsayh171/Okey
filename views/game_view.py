import arcade
from board_components.com import Com, COM_WIDTH
from board_components.stand import Stand
from engine.game import Game
import assets.colors as colr
from assets.utils import Views, ROUNDS
from views.game_view_graphics import GameViewGraphics

# Game window class
class GameView(arcade.View):
    """
    Main view for the program as the game is being played
    """
    def __init__(self, player_name):
        super().__init__()

        # create a new game
        self.game = Game(self.width, self.height)

        # get player name from previous screen
        self.player_name = player_name

        # Sprite list goes here
        self.com_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()

        # Non-sprite lists
        self.stand_slot_list = []
        self.com_stand_slot_list = []

        # Stand specifications
        self.player_stand = Stand()

        self.held_tiles = []

        self.open_displaying_player = None

        self.gui = GameViewGraphics(self.window, self.player_stand.total_stand_height)


    def setup(self):
        """Sets up the game"""
        self.game.set_player_name(self.player_name)
        self.game.start_new_round()

        self.game.players[0].open_stand.update()

        # Clear any existing sprites
        self.stand_slot_list.clear()
        self.tile_list.clear()

        # Stand coordinates
        self.stand_slot_list = self.player_stand.setup(self.width)
        print(len(self.stand_slot_list))
        # Com coordinates
        if self.game.curr_round == 1:
            self.setup_coms()

        self.setup_player_tiles()
        print(len(self.game.players[0].hand))

        self.hand_score = arcade.Text(
            str(self.game.turn.players[0].player_get_hand_score()),
            self.window.height * 0.03 + self.player_stand.total_stand_height * 0.75 * 0.5,
            self.window.height * 0.03 + self.player_stand.total_stand_height * 0.3,
            colr.THEME_TEAL,
            font_size=50,
            anchor_x="center",
            anchor_y="center",
        )

        self.game.turn.end_round = self.handle_round_end

    def on_show_view(self):
        self.background_color = colr.THEME_LIGHT_BLUE

    # Screen render that clears the board
    def on_draw(self):
        self.clear()

        self.player_stand.draw(self.stand_slot_list)

        # Draw coms
        for com in self.com_list:
            com.draw()

        # Draw discard piles
        for disc in self.game.discards:
            disc.draw()
            # Draw top tile
            if disc.tiles:
                tile = disc.tiles[len(disc.tiles) - 1]
                if disc is not self.game.players[0].discard_pile:
                    tile.center_x = disc.center_x
                    tile.center_y = disc.center_y
                # Set coordinates of tile to discard
                tile.tile_info.set_face_up()
                tile.draw()

        # Draw draw pile
        self.game.turn.draw_pile.draw()

        if self.open_displaying_player is not None:
            # Draw window box
            self.open_displaying_player.open_stand.draw_stand(self.width, self.height)

        self.gui.menu_button.draw()
        # Change open button if player can open
        if self.game.players[0].check_open(self.game.turn.open_score) or self.game.players[0].opened:
            self.gui.open_button.set_color(colr.THEME_YELLOW)
            self.gui.add_button.set_color(colr.THEME_YELLOW)
            self.gui.open_button.draw()
            self.gui.add_button.draw()
        else:
            self.gui.open_button.set_color(colr.GRAY)
            self.gui.add_button.set_color(colr.GRAY)
            self.gui.open_button.draw()
            self.gui.add_button.draw()

        # draw hand score
        arcade.draw_lbwh_rectangle_outline(self.window.height * 0.03,
                                           self.window.height * 0.03,
                                           self.player_stand.total_stand_height * 0.75,
                                           self.player_stand.total_stand_height * 0.75,
                                           colr.THEME_DARK_BLUE,
                                           3.0
                                           )
        self.gui.score_label.draw()

        self.hand_score.text = str(
            self.game.turn.players[0].hand_score
        )
        self.hand_score.draw()
        self.gui.end_turn_button.draw()

        # Minimum open score display
        self.gui.open_score.text = f"Minimum Open Score: {self.game.turn.open_score}"
        self.gui.open_score.draw()

        # Draw tiles at end on top of everything.
        for tile in self.tile_list:
            if (self.open_displaying_player is not None
                    and tile in self.game.players[0].discard_pile.tiles):
                continue
            tile.draw()

        if self.game.turn.get_current_player() is self.game.players[0] and self.game.turn.must_draw:
            self.game.turn.draw_pile.draw_highlight = True
        else:
            self.game.turn.draw_pile.draw_highlight = False

        # ui manager
        self.gui.manager.draw()

    def setup_player_tiles(self):
        """Sets up the player's tiles"""
        for i, tile in enumerate(self.game.players[0].hand):
            tile.set_curr_slot(self.stand_slot_list[i])
            self.stand_slot_list[i].holding_tile = True
            tile.tile_info.set_face_up()
            self.tile_list.append(tile)

    # Com setup
    def setup_coms(self):
        """Sets up the computers"""
        screen_width = self.width
        screen_height = self.height

        # Com coordinates
        com1_x = screen_width - COM_WIDTH
        com1_y = screen_height / 2
        com2_x = self.width / 2
        com2_y = screen_height - COM_WIDTH
        com3_x = COM_WIDTH
        com3_y = screen_height / 2

        # Make each com
        com1 = Com(com1_x, com1_y, colr.GRAY, self.game.players[1])
        com2 = Com(com2_x, com2_y, colr.GRAY, self.game.players[2])
        com3 = Com(com3_x, com3_y, colr.GRAY, self.game.players[3])

        # Add each com to the list
        self.com_list.append(com1)
        self.com_list.append(com2)
        self.com_list.append(com3)

        # Run com static method to assign com icons and names
        Com.assign_unique_icons(self.com_list)
        Com.assign_unique_names(self.com_list)

        for com in self.com_list:
            if com.player is not self.game.players[0]:
                com.player.name = com.name

    # Discard setup
    def setup_discard(self, player):
        """Sets up discard"""
        pass

    def remove_and_lock(self, player, group):
        """
        Helper function that clears previous hand position
        and removes from gui tile list when tiles go to open area.
        """
        for tile in group:
            if tile in player.hand:
                player.hand.remove(tile)

            if tile.current_slot:
                tile.current_slot.holding_tile = False

            if tile in self.tile_list:
                self.tile_list.remove(tile)

            tile.is_in_open = True

    def move_groups_to_open(self, player, groups, reset=False):
        """
        Helper function that moves valid groups from player's hand
        to open area.
        """
        if reset:
            player.open_tiles = [[], [], [], []] # 4 rows for open sets.
            for i, group in enumerate(groups):
                if i >= len(player.open_tiles):
                    break

                if len(group) < 3:
                    continue

                player.open_tiles[i] = list(group)
                self.remove_and_lock(player, group)
        else:
            # Fill empty rows
            for group in groups:
                if len(group) < 3:
                    continue

                for i in range(len(player.open_tiles)):
                    if len(player.open_tiles[i]) == 0:
                        player.open_tiles[i] = list(group)
                        self.remove_and_lock(player, group)
                        break

        player.open_stand.update()
        player.hand_score = 0 # resetting hand score

    def on_mouse_press(self, x, y, button, modifiers):
        # Prevents more clicking of player after end of turn
        if self.game.turn.get_current_player() != self.game.players[0]:
            return

        # when player must draw, allow clicking draw pile or discard pile
        if self.game.turn.must_draw:
            if not self.game.turn.draw_pile.collides_with_point((x, y)):
                prev_plyr_disc_click = False
                for discard in self.game.discards:
                    if discard.collides_with_point((x, y)) and discard.player_com_discard:
                        prev_plyr_disc_click = True
                        break
                if not prev_plyr_disc_click:
                    self.gui.show_popup("You must draw first")
                    return

        # TILE IS CLICKED
        clicked_tile = None
        for t in self.tile_list:
            if t.tile_clicked(x, y):
                clicked_tile = t

        # Lock tiles that have been taken to open space
        if clicked_tile and getattr(clicked_tile, "is_in_open", False):
            self.gui.show_popup("Opened tiles cannot be moved.")
            return

        if clicked_tile:
            # Prevent a player from picking up discarded tile after ending their turn
            for disc in self.game.discards:
                if clicked_tile in disc.tiles and self.game.turn.turn_ended:
                    self.gui.show_popup("Cannot move discarded tile after ending turn.")
                    return

            # Otherwise allow normal dragging
            self.held_tiles.append(clicked_tile)
            self.pull_to_top(clicked_tile)
            clicked_tile.highlight()
            return

        # ----------- Draw + discard -----------
        if self.open_displaying_player is None:

            # Check if draw pile was clicked
            if self.game.turn.draw_pile.collides_with_point((x, y)):
                self.game.turn.draw_pile.draw_highlight = False
                top_tile = self.game.turn.draw_tile()
                # If draw not allowed, stop
                if top_tile is None:
                    return
                print(f"Tile drawn from draw pile: {top_tile.tile_info.value}")

                # Add tile to gui hand
                for slot in self.stand_slot_list:
                    if not slot.holding_tile:
                        top_tile.center_x = slot.center_x
                        top_tile.center_y = slot.center_y
                        slot.holding_tile = True
                        top_tile.current_slot = slot
                        top_tile.tile_info.set_face_up()
                        self.tile_list.append(top_tile)
                        break
                return

            # Check if discard player accesses was clicked
            for discard in self.game.discards:
                # Check if clicked on discard not for player to access
                if discard.collides_with_point((x, y)):
                    print(self.game.turn.get_current_player().opened)
                    if not discard.player_com_discard:
                        self.gui.show_popup("You can only draw from the player "
                                            "to your left's discard.")
                        continue
                    if not self.game.turn.get_current_player().opened:
                        self.gui.show_popup("Only players who have opened may draw"
                                            " from a discard pile.")
                        return
                    top_tile = self.game.turn.draw_from_discard(discard)
                    if top_tile is None:
                        return
                    print(f"Drawn from discard pile: {top_tile.tile_info.value}")
                    if top_tile not in self.tile_list:
                        self.tile_list.append(top_tile)

                    top_tile.tile_info.set_face_up()

                    # Add tile to gui hand
                    for slot in self.stand_slot_list:
                        if not slot.holding_tile:
                            top_tile.center_x = slot.center_x
                            top_tile.center_y = slot.center_y
                            slot.holding_tile = True
                            top_tile.current_slot = slot
                            break
                    return

        # Check if clicked on com
        for com in self.com_list:
            if com.collides_with_point((x, y)):
                if not com.player.opened:
                    self.gui.show_popup("This player has not opened.")
                    return

                # No coms are displaying their hand
                if self.open_displaying_player is None:
                    # Display hand
                    self.open_displaying_player = com.player
                    com.player.open_stand.update()
                    return

                # Closing currently open com window
                if self.open_displaying_player == com.player:
                    self.open_displaying_player = None
                    return

        # ---------- 'Add' button pressed ----------
        if self.gui.add_button.button_pressed(x, y):

            player = self.game.turn.get_current_player()

            if not player.opened:
                self.gui.show_popup("You must open first")
                return

            if player.opened_this_turn:
                self.gui.show_popup("Cannot add on same turn as opening")
                return

            player.player_get_hand_score()
            groups = player.arranged_groups

            if not groups:
                self.gui.show_popup("No valid groups to add")
                return

            self.move_groups_to_open(player, groups, reset=False)

            print("Added groups to open")
            return

        # ---------- 'Open' button pressed ----------
        if self.gui.open_button.button_pressed(x, y):
            # Allows valid arranged groups from hand to open,

            player = self.game.turn.get_current_player()

            # ---- player has opened
            if player.opened:
                if self.open_displaying_player == player:
                    self.open_displaying_player = None # close
                else:
                    player.open_stand.update()
                    self.open_displaying_player = player
                return

            # ---- player has not opened
            # use gui-based scoring when player arranges tiles
            score = player.player_get_hand_score()

            if score < self.game.turn.open_score: # temp number for testing
                self.gui.show_popup(f"Not enough points to open. Reach {self.game.turn.open_score}")
                return

            groups = player.arranged_groups

            if not groups:
                self.gui.show_popup("No valid arranged groups to open with")
                return

            self.move_groups_to_open(player, groups, reset=True) # call helper function

            player.opened = True # mark player as opened
            player.opened_this_turn = True
            self.open_displaying_player = player # display open window

            print(f"{player.name} opened with {score} points!")
            if player.is_player_ai:
                self.gui.show_popup(f"{player.name} opened with {score} points")

            return

        # ---------- 'End Turn' button pressed ----------
        if self.gui.end_turn_button.button_pressed(x, y):
            # Make sure no open window is displaying before ending turn
            if self.open_displaying_player is None:
                player = self.game.turn.get_current_player()
                disc = player.discard_pile

                # Visual tile must be in discard
                if not disc.tiles:
                    self.gui.show_popup(f"Please place a tile in discard before ending your turn.")
                    return

                # Get the tile that is visually in discard
                tile = disc.tiles[-1]

                if tile not in player.hand:
                    self.gui.show_popup("You must place a *new* tile in discard before ending your turn.")
                    return

                # Remove discarded tile from held tiles
                if tile in self.held_tiles:
                    self.held_tiles.remove(tile)
                    tile.unhighlight()

                # Don't draw tile over open display
                if tile in self.tile_list:
                    self.tile_list.remove(tile)

                # Handing discard to game logic
                self.game.turn.discard_tile(tile)
                self.game.turn.end_turn()

        # check if menu was clicked
        if self.gui.menu_button.button_pressed(x, y):
            self.window.show_menu(self)

    def on_mouse_release(self, x, y, button, modifiers):
        # Show button press if clicked on end turn
        if self.gui.end_turn_button.button_pressed(x, y) :
            self.gui.end_turn_button.show_pressed_button(colr.GRAY)

        # If no cards are being held, return
        if len(self.held_tiles) == 0:
            return

        tile = self.held_tiles[0]
        player = self.game.turn.get_current_player()
        disc = player.discard_pile

        # remove tile from discard list if was in disc
        if tile in disc.tiles and not disc.tile_overlaps(tile):
            disc.tiles.remove(tile)
            disc.holding_tile = False

            tile.current_slot = None

            if tile not in player.hand:
                player.hand.append(tile)

        # get set of slots
        available_slots = list(self.stand_slot_list)
        if self.open_displaying_player is not None:
            for slot in self.open_displaying_player.open_stand.slots:
                if (not slot.holding_tile and
                        len(self.open_displaying_player.open_stand.tiles[slot.open_row_index]) > 0):
                    available_slots.append(slot)

        # Snap tile to the closest stand slot or a com hand if displayed
        # check if tile touching slot
        touching_slot = None
        for slot in available_slots:
            is_open_slot = getattr(slot, "open_row_index", None) is not None
            # slot is open rack
            if is_open_slot:
                # Open slots can be expanded
                if slot.tile_overlaps(tile):
                    touching_slot = slot
                    break
            # slot is player hand
            else:
                # Only empty slots
                if not slot.holding_tile and slot.tile_overlaps(tile):
                    touching_slot = slot
                    break

        touching_discard = disc.tile_overlaps(tile)

        # Tile snapping if an open window is displaying
        if self.open_displaying_player is not None and touching_slot:

            row_index = touching_slot.open_row_index

            # address TypeError
            if row_index is not None: # open racks

                current_player = self.game.turn.get_current_player()

                # Block same turn adding tiles to open
                if current_player.opened_this_turn:
                    self.gui.show_popup("Cannot add tiles on the same turn you opened. "
                                        "Add at your next turn")
                    self.snap(tile, self.stand_slot_list) # snap only back to hand
                    self.held_tiles = []
                    tile.unhighlight()
                    return

                # block adding to any open racks if player has not opened yet
                if not current_player.opened:
                    self.gui.show_popup("You must open before adding to another player's tiles.")
                    self.snap(tile, self.stand_slot_list) # snap only back to hand
                    self.held_tiles = []
                    tile.unhighlight()
                    return

                target_player = self.open_displaying_player
                row = target_player.open_tiles[row_index]

                # ---------- Existing group ----------
                if len(row) > 0: # if row already has a group
                    success = self.game.turn.try_add_tile_to_group(tile, target_player, row_index)

                    if not success:
                        print("Invalid move: does not fit this open group")
                        self.snap(tile, self.stand_slot_list)
                        self.held_tiles = []
                        tile.unhighlight()
                        return

                    if tile in self.tile_list:
                        self.tile_list.remove(tile) # remove from gui

                    if tile in current_player.hand:
                        current_player.hand.remove(tile) # remove from hand

                    tile.is_in_open = True
                    target_player.open_stand.update()
                # ---------- Existing group ----------

            else:
                self.snap(tile, available_slots)

                if tile not in player.hand:
                    player.hand.append(tile)

        # Tile snapping if no open window is displaying
        else:
            # If tile is over discard
            if touching_discard and not touching_slot:

                # block access to discard except first player
                if self.game.turn.must_draw:
                    self.gui.show_popup("You must draw before discarding")
                    self.snap(tile, available_slots)
                    self.held_tiles = []
                    tile.unhighlight()
                    return

                # allow discard access after draw
                self.snap(tile, [disc])

                if tile not in disc.tiles:
                    disc.tiles.append(tile)

                disc.holding_tile = True

            # If tile is touching a stand slot
            elif touching_slot:
                self.snap(tile, available_slots)
                if tile not in player.hand:
                    player.hand.append(tile)
            else:
                self.snap(tile, available_slots)

        self.held_tiles = []
        tile.unhighlight()

        player = self.game.turn.players[0]
        player.hand_score = player.player_get_hand_score()

    def on_mouse_motion(self, x, y, dx, dy):
        for moving_tile in self.held_tiles:
            moving_tile.center_x += dx
            moving_tile.center_y += dy

    def pull_to_top(self, selected_tile: arcade.Sprite):
        self.tile_list.remove(selected_tile)
        self.tile_list.append(selected_tile)

    def snap(self, tile, selected_list):
        """Snaps a tile to a slot location"""
        reset_position = True

        # find the closest spot by looping through list
        available_slots = list(selected_list)
        slot, _ = arcade.get_closest_sprite(tile, available_slots)

        while available_slots and reset_position:
            # if closest slot is empty and tile is on top of it at all, snap
            if not slot.holding_tile and slot.tile_overlaps(tile):
                tile.position = slot.center_x, slot.center_y
                slot.holding_tile = True

                # reset previous slot before changing curr slot to new location
                if tile.current_slot is not None:
                    prev_slot = tile.current_slot
                    prev_slot.holding_tile = False

                    row_index = prev_slot.open_row_index
                    if row_index is not None and self.open_displaying_player is not None:
                        row = self.open_displaying_player.open_tiles[row_index]
                        if tile in row:
                            row.remove(tile)
                            self.open_displaying_player.open_stand.update()
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
            if tile.current_slot is not None:
                tile.position = tile.current_slot.center_x, tile.current_slot.center_y

    def tile_clicked(self, x, y, tile):
        """Returns the location of a tile when it is clicked"""
        return (tile.center_x - tile.width < x < tile.center_x + self.width
                and tile.center_y - self.height < y < tile.center_y + self.height)

    def handle_round_end(self):
        if self.game.curr_round < ROUNDS:
            self.game.curr_round += 1
            self.window.show_scoreboard(Views.GAME, self.game, self, True)
        else:
            self.window.show_end(self.game, False)

import arcade
from board_components.com import Com, COM_WIDTH
from board_components.stand import Stand
from engine.game import Game
from engine.tile import Tile, TileInfo
import assets.colors as colr
from views.game_view_graphics import GameViewGraphics

# Game window class
class GameView(arcade.View):
    """
    Main view for the program as the game is being played
    """
    def __init__(self, player_name):
        super().__init__()

        # create a new game
        self.game = None

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

        self.player_discard = None

        self.player_hand = None

        self.open_displaying_player = None

        self.gui = GameViewGraphics(self.window, self.player_stand.total_stand_height)
        self.hand_score = None


    # Set up game
    def setup(self):
        # need to do this here so width and height are set up
        self.game = Game(self.width, self.height)
        self.game.set_player_name(self.player_name)
        self.game.start_game()

        # TODO: DELETE THESE TWO LINES, ONLY HERE FOR TESTING PLAYER OPEN
        self.game.players[0].can_open = True
        self.game.players[0].open_tiles = [[Tile(TileInfo(3, arcade.color.RED, "♥")),
                                            Tile(TileInfo(3, arcade.color.RED, "♥"))], [], [],
                                           []]

        self.game.players[0].open_stand.update()

        # Clear any existing sprites
        self.stand_slot_list.clear()
        self.tile_list.clear()
        self.com_list.clear()

        # Stand coordinates
        self.stand_slot_list = self.player_stand.setup(self.width)
        # Com coordinates
        self.setup_coms()

        self.setup_player_tiles()

        self.hand_score = arcade.Text(
            str(self.game.turn.get_current_player().hand_score),
            self.window.height * 0.03 + self.player_stand.total_stand_height * 0.75 * 0.5,
            self.window.height * 0.03 + self.player_stand.total_stand_height * 0.3,
            colr.THEME_TEAL,
            font_size=50,
            anchor_x="center",
            anchor_y="center",
        )

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
        if self.game.players[0].can_open:
            self.gui.open_button.set_color(colr.THEME_YELLOW)
            self.gui.open_button.draw()
        else:
            self.gui.open_button.set_color(colr.GRAY)
            self.gui.open_button.draw()

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
            self.game.turn.get_current_player().hand_score
        )
        self.hand_score.draw()
        self.gui.end_turn_button.draw()

        # Draw tiles at end on top of everything.
        for tile in self.tile_list:
            tile.draw()

    def setup_player_tiles(self):
        for i, tile in enumerate(self.game.players[0].hand):
            tile.set_curr_slot(self.stand_slot_list[i])
            self.stand_slot_list[i].holding_tile = True
            tile.tile_info.set_face_up()
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

    # Discard setup
    def setup_discard(self, player):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        # prevents more clicking of player after end of turn
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
                    print("You must draw first")
                    return

        # TILE IS CLICKED
        clicked_tile = None
        for t in self.tile_list:
            if t.tile_clicked(x, y):
                clicked_tile = t
        if clicked_tile:
            # prevent a player from picking up discarded tile after ending their turn
            for disc in self.game.discards:
                if clicked_tile in disc.tiles and self.game.turn.turn_ended:
                    print("Cannot move discarded tile after ending turn")
                    return

            # Otherwise allow normal dragging
            self.held_tiles.append(clicked_tile)
            self.pull_to_top(clicked_tile)
            clicked_tile.highlight()
            return

        # ---- Draw + discard
        if self.open_displaying_player is None:

            # Check if draw pile was clicked
            if self.game.turn.draw_pile.collides_with_point((x, y)):
                # make Game handle draw logic
                top_tile = self.game.turn.draw_tile()
                # if draw not allowed, stop
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
                    if not discard.player_com_discard:
                        continue
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
            # TODO: Once a boolean for player being open, add and statement to check
            if com.collides_with_point((x, y)):

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

        # Check if open button was clicked
        if self.gui.open_button.button_pressed(x, y) and self.game.players[0].can_open:
            # See if any open window is displaying
            if self.open_displaying_player is None:
                self.game.players[0].open_stand.update()

                self.open_displaying_player = self.game.players[0]

            # Stop displaying player open window
            else:
                self.open_displaying_player = None
            return

        # Check if end_turn button was clicked
        if self.gui.end_turn_button.button_pressed(x, y):

            player = self.game.turn.get_current_player()
            disc = player.discard_pile

            # must have visually placed a tile in discard
            if not disc.tiles:
                print("Please place a tile in discard before ending your turn")
                return

            # get the tile that is visually in discard
            tile = disc.tiles[-1]

            if tile not in player.hand:
                print("You must place a *new* tile in discard before ending your turn")
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
            # now end turn
            self.game.turn.end_turn()
            return

        # check if menu was clicked
        if self.gui.menu_button.button_pressed(x, y):
            self.window.show_menu(self)

    def on_mouse_release(self, x, y, button, modifiers):
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
            if not slot.holding_tile and slot.tile_overlaps(tile):
                touching_slot = slot
                break

        touching_discard = disc.tile_overlaps(tile)

        # Tile snapping if an open window is displaying
        if self.open_displaying_player is not None:
            if touching_slot:
                row_index = touching_slot.open_row_index
                open_edge = getattr(touching_slot, "open_edge", None)
                row = self.open_displaying_player.open_tiles[row_index]
                if open_edge == "before":
                    row.insert(0, tile)
                else:
                    row.append(tile)
                self.tile_list.remove(tile)
                self.snap(tile, available_slots)
                self.open_displaying_player.open_stand.update()
            else:
                # snap tile back to original position
                self.snap(tile, available_slots)

        # Tile snapping if no open window is displaying
        else:
            # If tile is over discard
            if touching_discard and not touching_slot:

                # block access to discard except first player
                if self.game.turn.must_draw:
                    print("You must draw before discarding")
                    # send tile back to stand
                    self.snap(tile, available_slots)

                    self.held_tiles = []
                    tile.unhighlight()
                    return
                # allow discard access after draw
                self.snap(tile, [disc])

                if tile not in disc.tiles:
                    disc.tiles.append(tile)
                #
                # if tile in player.hand:
                #     player.hand.remove(tile)

                disc.holding_tile = True

            # If tile is touching a stand slot
            elif touching_slot:
                self.snap(tile, available_slots)
                if tile not in player.hand:
                    player.hand.append(tile)
            # Else nowhere to snap so send it back to original spot
            else:
                # Snap back to original slot
                self.snap(tile, available_slots)

        self.held_tiles = []
        tile.unhighlight()
        self.game.turn.get_current_player().player_get_hand_score()

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
        return (tile.center_x - tile.width < x < tile.center_x + self.width
                and tile.center_y - self.height < y < tile.center_y + self.height)
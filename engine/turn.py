import arcade
from assets.utils import INITIAL_OPEN, STARS_OPEN

class Turn:
    """
    Manages a single turn in the game
    """
    def __init__(self, players):
        self.players = players
        self.draw_pile = None

        # -------- Turn system --------
        self.current_player_idx = 0  # to track turn of player
        self.last_discard = None  # track most recently discarded tile
        self.must_draw = False  # check if player must draw before discarding
        self.turn_ended = False  # to track if discard is finalized
        self.has_discarded = False # to track if a player discarded in their turn
        self.open_score = INITIAL_OPEN #Starts at 81

    def get_current_player(self):
        """
        returns the player who is in their turn currently
        """
        return self.players[self.current_player_idx]

    def new_round(self, start_player):
        """Sets all the variables for a new round"""
        # set turn to starting player (at start, current player is the starting player)
        self.current_player_idx = start_player
        self.open_score = INITIAL_OPEN

        # at start, no previous discard yet
        self.last_discard = None

        # first player starts with 15, no draw here
        self.must_draw = False
        self.turn_ended = False

    def discard_tile(self, tile):
        """
        function discards a tile and ends the turn
        """

        player = self.get_current_player()

        # player must draw before discarding (except for first turn)
        if self.must_draw:
            print("Draw before discarding tile")
            return

        # Remove tile from player's hand
        if tile in player.hand:
            player.hand.remove(tile)

        # save last discarded tile for next player to possibly take
        self.last_discard = tile

        # update to only show last tile
        player.discard_pile.tiles.append(tile) # add tile player just discarded
        player.discard_pile.holding_tile = False

        print(f"{player.name} placed {tile.tile_info.value} in their discard")
        print(f"--- End of {player.name}'s turn ---")
        self.has_discarded = True

    def draw_tile(self, delta_time = 2):
        """
        function that handles the action of drawing a tile from middle pile
        """
        # check that game is not done

        player = self.get_current_player()

        # block drawing if a player is not allowed
        # first player starts with 15 (no draw here)
        if not self.must_draw:
            print("Not allowed to draw right now.")
            return None

        # prevent multiple drawing
        if player.drawn:
            return None

        if self.draw_pile.count() == 0:
            return None

        # draw from pile
        tile = self.draw_pile.draw_tile()
        player.hand.append(tile)

        # mark that player has drawn
        player.drawn = True

        # after drawing, must discard
        self.must_draw = False

        self.turn_ended = False

        print(f"{player.name} drew {tile.tile_info.value} from middle pile")

        return tile

    def draw_from_discard(self, discard):
        """
        Draw a tile from a discard pile
        """

        player = self.get_current_player()

        if not self.must_draw:
            print("Not allowed to draw right now")
            return None

        if player.drawn:
            print("Tile already drawn for your turn")
            return None

        if len(discard.tiles) == 0:
            print("Discard pile is empty")
            return None

        # drawing tile
        tile = discard.draw_tile()
        player.hand.append(tile)

        # update state
        player.drawn = True
        self.must_draw = False
        self.turn_ended = False

        previous_player = self.players[(self.current_player_idx - 1) % len(self.players)]
        print(f"{player.name} drew {tile.tile_info.value} from {previous_player.name}'s discard")

        return tile

    def end_turn(self):
        """
        Finalizes the turn of a player by validating rules.
        Locks player's arranged valid tile groupings
        """

        player = self.get_current_player()

        # validate that player indeed discarded
        if not self.has_discarded:
            print("Please discard a tile before ending your turn")
            return

        # Updates open score if real player opened
        if not player.is_player_ai and player.opened_this_turn:
            if player.hand_score >= self.open_score:
                self.open_score = player.hand_score

        player.opened_this_turn = False

        # moves to next player (circular)
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

        # get next player
        next_player = self.get_current_player()

        # Reset all discard access
        for p in self.players:
            p.discard_pile.player_com_discard = False

        # Allow only previous player's discard
        previous_player = self.players[(self.current_player_idx - 1) % len(self.players)]
        previous_player.discard_pile.player_com_discard = True

        # ---- Resetting turn state for next player
        self.must_draw = True # next player must draw
        self.has_discarded = False # reset discard tracking
        self.turn_ended = True # allow dragging back
        player.drawn = False # next player hasn't drawn yet

        print(f"\n--- {next_player.name}'s turn ---")
        print(f"Open score: {self.open_score}")
        print(f"Open Status: {next_player.opened}")

        if self.is_round_over():
            self.end_round()
            return

        # If the current player is AI, run the com turn logic
        if next_player.is_player_ai:
            arcade.schedule_once(self.com_turn, 1)

    def com_turn(self, delta_time = 2):
        """Handles AI player's full turn."""
        player = self.get_current_player()
        print(f"AI player's turn: {player.name}")

        if player.get_hand_score() >= self.open_score:
            #print(f"{player.hand_score}")
            self.open_score = player.hand_score
            if self.open_score >= STARS_OPEN and self.is_first_open():
                player.stars += 1
            player.open()

        if player.opened:
            arcade.schedule_once(self.com_open_turn, 1)
        else:
            arcade.schedule_once(self.draw_tile, 1)
            arcade.schedule_once(self.com_discard, 2)

    def com_discard(self, delta_time = 2):
        """Logic for computer discarding"""
        player = self.get_current_player()
        # Gets the hand score and determines which tiles are being used for scoring
        #print(player.hand_score)
        # -----2. Discard
        # Runs the com discard function
        self.discard_tile(player.com_discard_tile())

        if self.has_discarded:
            self.end_turn()

    def com_open_turn(self, delta_time = 2):
        """Logic for what a computer does on a turn if they have opened"""
        player = self.get_current_player()
        previous_player = self.players[(self.current_player_idx - 1) % len(self.players)]
        if not player.drawn:
            for target_player in self.players:
                if not target_player is player:
                    continue
                for group_index in range(len(target_player.open_tiles)):
                    if self.try_add_tile_to_group(self.last_discard, target_player, group_index):
                        self.draw_from_discard(previous_player.discard_pile)
                        break
                if player.drawn:
                    break
        if not player.drawn:
            arcade.schedule_once(self.draw_tile, 1)
        player.add_valid_tiles_to_open()
        self.add_to_other_open(player)
        player.print_open_tiles()
        arcade.schedule_once(self.com_discard, 2)

    def try_add_tile_to_group(self, tile, target_player, group_index):
        """Tries to add a given tile to an existing group in a player's open"""
        group = target_player.open_tiles[group_index]

        if tile is None or not group:
            return False

        is_set = all(t.tile_info.value == group[0].tile_info.value for t in group)
        is_run = all(t.tile_info.color == group[0].tile_info.color for t in group)

        # SET RULE
        if is_set:
            if tile.tile_info.value != group[0].tile_info.value:
                return False

            colors = {t.tile_info.color for t in group}
            if tile.tile_info.color in colors:
                return False

            group.append(tile)
            return True

        # RUN RULE
        if is_run:
            if tile.tile_info.color != group[0].tile_info.color:
                return False

            values = sorted(t.tile_info.value for t in group)

            if tile.tile_info.value == values[0] - 1:
                group.insert(0, tile)
                return True

            if tile.tile_info.value == values[-1] + 1:
                group.append(tile)
                return True

        return False

    def add_to_other_open(self, player):
        """
        During AI turn: attempt to extend ANY player's open tiles
        using ALL tiles in AI hand.
        """
        moved = True

        while moved:
            moved = False

            for tile in player.hand[:]:   # all tiles

                if tile is None:
                    continue

                for target_player in self.players:   # ALL players
                    if not target_player is player:
                        continue

                    for group_index in range(len(target_player.open_tiles)):

                        if self.try_add_tile_to_group(tile, target_player, group_index):

                            player.hand.remove(tile)
                            moved = True
                            print(f"Added {tile.tile_info.value} to {target_player.name}'s open")

                            # Restart scanning after any successful move
                            break

                    if moved:
                        break

                if moved:
                    break

    def is_round_over(self):
        """Checks if a round is over
            by checking if any player's hand is empty
            or the draw pile is empty"""
        round_over = False
        if self.draw_pile.count() == 0:
            round_over = True

        for player in self.players:
            if player.check_complete():
                round_over = True

        if round_over:
            for player in self.players:
                player.calculate_round_score()

        return round_over

    def is_first_open(self):
        for p in self.players:
            if p.opened:
                return False
        return True

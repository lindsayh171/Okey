import time

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

    def get_current_player(self):
        """
        returns the player who is in their turn currently
        """
        return self.players[self.current_player_idx]

    def new_round(self, start_player):
        # set turn to starting player (at start, current player is the starting player)
        self.current_player_idx = start_player

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
        #else:
        #    raise ValueError("Tile not in hand to be discarded")

        # save last discarded tile for next player to possibly take
        self.last_discard = tile

        # update to only show last tile
        player.discard_pile.tiles.clear() # remove everything in discard pile
        player.discard_pile.tiles.append(tile) # add tile player just discarded
        player.discard_pile.holding_tile = False

        print(f"{player.name} placed {tile.tile_info.value} in discard (NOT FINAL)")

    def draw_tile(self):
        """
        function that handles the action of drawing a tile from middle pile
        """
        player = self.get_current_player()

        # block drawing if a player is not allowed
        # first player starts with 15 (no draw here)
        if not self.must_draw:
            print("Not allowed to draw right now")
            return None

        # prevent multiple drawing
        if player.drawn:
            print("Tile already drawn for your turn")
            return None

        if self.draw_pile.count() == 0:
            print("Draw pile is empty")
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

        print(f"{player.name} drew {tile.tile_info.value} from discard pile")

        return tile

    def end_turn(self):
        """
        Finalizes the turn of a player by validating rules.
        Locks player's arranged valid tile groupings
        """
        self.turn_ended = True

        player = self.get_current_player()

        # validate that player indeed discarded
        if not player.discard_pile.tiles:
            print("Please discard a tile before ending your turn")
            return

        # Lock score at what player last arranged for their tiles
        player.locked_score = player.player_get_hand_score()

        # reset draw flag for current player before moving to next
        player.drawn = False

        # moves to next player (circular)
        self.current_player_idx = (self.current_player_idx - 1) % len(self.players)

        # After first turn, all players draw before discarding
        self.must_draw = True

        print(f"Next player's turn: {self.get_current_player().name}")
        # self.debug_state()
        # If the current player is AI, run the com turn logic
        if self.get_current_player().is_player_ai:
            self.com_turn()

    def com_turn(self):
        """Handles AI player's full turn."""
        player = self.get_current_player()
        self.draw_tile()
        # Simulated wait time
        time.sleep(2)
        # Gets the hand score and determines which tiles are being used for scoring
        player.get_hand_score()
        # TODO: Add opening logic here
        # Simulated wait time
        time.sleep(2)
        # Runs the com discard function
        self.discard_tile(player.com_discard_tile())
        self.end_turn()

"""
Controls the main gameplay logic
"""
from engine.dealer import Dealer
from engine.player import Player
from engine.discard_pile import DiscardPile
from engine.tile import TILE_WIDTH

class Game:
    """
    Keeps track of all aspects of game
    """
    def __init__(self, window_width, window_height):
        # window dimensions
        self.window_width = window_width
        self.window_height = window_height

        self.discards = self.discard_setup()

        # To note what discard pile player can access
        self.discards[1].player_com_discard = True

        self.players = [Player(self.discards[0], "Person", False),
                        Player(self.discards[1],"Com_1", True),
                        Player(self.discards[2],"Com_2", True),
                        Player(self.discards[3],"Com_3", True)]

        # TODO: allow someone to pick their own name
        # TODO: generate fun computer names
        self.dealer = Dealer()
        self.draw_pile = None

        # -------- Turn system --------
        self.current_player_idx = 0 # to track turn of player
        self.last_discard = None # track most recently discarded tile
        self.must_draw = False # check if player must draw before discarding
        self.turn_ended = False # to track if discard is finalized

    def start_new_round(self, starting_player_idx=0):
        """
        Starts a new round
        """
        # Dealer deals cards to the player and computers after
        # building tiles and randomizing. Returns remaining draw pile.
        self.draw_pile = self.dealer.deal_new_round(self.players, starting_player_idx)

        # set turn to starting player (at start, current player is the starting player)
        self.current_player_idx = starting_player_idx

        # at start, no previous discard yet
        self.last_discard = None

        # first player starts with 15, no draw here
        self.must_draw = False
        self.turn_ended = False
        # print(f"\n *** NEW ROUND ***")
        # print(f"Starting player: {self.players[self.current_player_idx].name}")

    def discard_setup(self):
        """
        Helper function to set up discards
        :return:
        """
        # Discard pile coordinates
        # Placing discards on thirds of the screen size
        third_width = self.window_width / 3
        third_height = self.window_height / 3

        left_disc_x = third_width - TILE_WIDTH
        right_disc_x = third_width * 2 + TILE_WIDTH
        top_disc_y = third_height * 2
        bottom_disc_y = third_height

        discards = [DiscardPile(right_disc_x, bottom_disc_y, ),
                     DiscardPile(left_disc_x, bottom_disc_y, ),
                     DiscardPile(right_disc_x, top_disc_y, ),
                     DiscardPile(left_disc_x, top_disc_y, )]
        return discards

    def set_player_name(self, name):
        self.players[0].name = name

    def start_game(self):
        """
        Loops through rounds but for now it does just one
        :return:
        """
        # TODO: loop continuing to deal new rounds while round is not ended
        self.start_new_round()

    def get_current_player(self):
        """
        returns the player who is in their turn currently
        """
        return self.players[self.current_player_idx]

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

        print(f"{player.name} placed {tile.value} in discard (NOT FINAL)")

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
        tile = self.draw_pile.draw()
        player.hand.append(tile)

        # mark that player has drawn
        player.drawn = True

        # after drawing, must discard
        self.must_draw = False

        self.turn_ended = False

        print(f"{player.name} drew {tile.value} from middle pile")

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

        print(f"{player.name} drew {tile.value} from discard pile")

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
        self.debug_state()

    def debug_state(self):
        """
        Prints game state in readable format
        """

        print("\n========== GAME STATE ==========")

        current_idx = self.current_player_idx
        current_player = self.get_current_player()

        # Focus more on human player (index 0)
        player = self.players[0]

        print(f"\n--- Player [0] {player.name} ---")
        print(f"Hand Size: {len(player.hand)}")
        print(f"Drawn This Turn: {player.drawn}")

        # Scores
        arranged_score = player.player_get_hand_score()
        print(f"GUI tile arrangement Score: {arranged_score}")
        print(f"Locked Score: {player.locked_score}")

        # Discard
        if player.discard_pile.tiles:
            top_tile = player.discard_pile.tiles[-1]
            print(f"Top Discard: {top_tile.value}")
        else:
            print("Top Discard: None")

        print(f"Turn Ended: {self.turn_ended}")

        # Draw pile
        if self.draw_pile:
            print(f"Draw Pile Count: {self.draw_pile.count()}")

        print("================================\n")

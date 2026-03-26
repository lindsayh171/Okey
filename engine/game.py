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

        self.players = [Player(self.discards[0], self.enter_player_name(), False),
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

    def start_new_round(self, starting_player_idx=0):
        """
        Starts a new round
        :param starting_player_idx:
        :return:
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

    def enter_player_name(self):
        name = "Player"
        # TODO: pop-up to ask for player name
        return name

    def start_game(self):
        """
        Loops through rounds but for now it does just one
        :return:
        """
        # TODO: loop continuing to deal new rounds while round is not ended
        self.start_new_round()

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def debug_state(self):
        """
        Prints game state for debugging
        """

        print("\n========== GAME STATE ==========")

        # Turn info
        print(f"Current Player Index: {self.current_player_idx}")
        print(f"Current Player: {self.get_current_player().name}")
        print(f"Must Draw: {self.must_draw}")

        if self.last_discard:
            print(f"Last Discard: {self.last_discard.value} ({self.last_discard.color})")
        else:
            print("Last Discard: None")

        print("\n--- PLAYERS ---")

        for i, player in enumerate(self.players):
            marker = " <-- CURRENT" if i == self.current_player_idx else ""

            print(f"[{i}] {player.name}{marker}")
            print(f"   Hand Size: {len(player.hand)}")
            print(f"   Hand Score (logic): {player.get_hand_score()}")
            print(f"   Drawn This Turn: {player.drawn}")

            print("   Tiles:",
                  [(t.value, t.color) for t in player.hand])

            print("")

        print(f"Draw Pile Count: {self.draw_pile.count()}")

        print("================================\n")


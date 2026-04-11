"""
Controls the main gameplay logic
"""
from engine.dealer import Dealer
from engine.player import Player
from engine.discard_pile import DiscardPile
from engine.tile import TILE_WIDTH
from engine.turn import Turn

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
        self.discards[3].player_com_discard = True

        self.players = [Player(self.discards[0], "Person", False),
                        Player(self.discards[1],"Com_1", True),
                        # com 2 and 3 discard were displaying in opposite places on board
                        Player(self.discards[2],"Com_2", True),
                        Player(self.discards[3],"Com_3", True)]

        self.dealer = Dealer(self.window_width, self.window_height)
        self.turn = Turn(self.players)
        self.curr_round = 1

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
                     DiscardPile(right_disc_x, top_disc_y, ),
                     DiscardPile(left_disc_x, top_disc_y, ),
                     DiscardPile(left_disc_x, bottom_disc_y, )]
        return discards

    def set_player_name(self, name):
        """Sets the player's name to the inputed name"""
        self.players[0].name = name

    def start_new_round(self, starting_player_idx=0):
        """
        Starts a new round
        """
        # reset player hands
        for player in self.players:
            player.reset()

        # reset discards
        for discard in self.discards:
            discard.tiles = []

        # Dealer deals cards to the player and computers after
        # building tiles and randomizing. Returns remaining draw pile.
        self.turn.draw_pile = self.dealer.deal_new_round(self.players, starting_player_idx)

        self.turn.new_round(starting_player_idx)

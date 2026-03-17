"""
Controls the main gameplay logic
"""
from engine.board import Board
from engine.dealer import Dealer
from engine.player import Player
from engine.draw_pile import DrawPile
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
        self.players = [Player(self.discards[0], self.enter_player_name(), False),
                        Player(self.discards[1],"Com_1", True),
                        Player(self.discards[2],"Com_2", True),
                        Player(self.discards[3],"Com_3", True)]

        # TODO: allow someone to pick their own name
        # TODO: generate fun computer names
        self.board = Board(self.players, 0)
        self.dealer = Dealer()

        # initialize a list of tiles
        self.tiles = self.dealer.build_okey_set()

        # create draw pile - put all tiles in draw pile for now
        self.draw_pile = DrawPile(self.tiles)

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

    def play_game(self):
        # TODO: loop continuing to deal new rounds while round is not ended
        self.dealer.deal_new_round(self.players)

# Dealer "builds" the 106 tiles, randomly shuffles
# Deals 14 to each player,
# except a single player whom Dealer gives 15
# Puts back the remaining tiles in the draw_pile (middle pile)

import random

from tile import Tile
from player import Player
from draw_pile import DrawPile
from board import Board

class Dealer:
    def __init__(self):
        self.rng = random.Random()

    def build_okey_set(self):
        # 106 total tiles
        # Numbers 1-13; 2 copies of each
        # 2 jokers
        # 4 colors

        tiles = []
        for i in range(0,4):
            for number in range(1, 14):
                # appending two copies of each tile
                tiles.append(Tile(Tile.colors[i], number, Tile.suits[i], False, 0))
                tiles.append(Tile(Tile.colors[i], number, Tile.suits[i], False, 1))

        # Adding the jokers
        tiles.append(Tile(None, None, None, True, 0)) # joker holding value to be implemented later
        tiles.append(Tile(None, None, None, True, 1))

        return tiles

    # Dealer to set up a new round,
    def deal_new_round(self, player_names, starting_player_idx = 0):
        if len(player_names) != 4:
            raise AttributeError('Okey game requires four players.')

        # creating player objs
        players = []
        for name in player_names:
            players.append(Player(name))

        # Build + shuffle
        tiles = self.build_okey_set()
        self.rng.shuffle(tiles)

        # Deal 14 tiles to each player
        for i in range(14):
            for player in players:
                player.draw_tile(tiles.pop())

        # Starting player is dealt 15 tiles
        players[starting_player_idx].draw_tile(tiles.pop())

        # remaining tiles go on draw pile
        draw_pile = DrawPile(tiles)

        # return board state for the round
        return Board(players, draw_pile, starting_player_idx)









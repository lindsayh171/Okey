# Dealer "builds" the 106 tiles, randomly shuffles
# Deals 14 to each player,
# except a single player whom Dealer gives 15
# Puts back the remaining tiles in the draw_pile (middle pile)

import random

from engine.tile import Tile, TILE_COLORS_SYMBOLS, TileInfo
from engine.draw_pile import DrawPile
import assets.colors as colr

class Dealer:
    """
    TODO: make docstring
    """
    def __init__(self, width, height):
        self.window_width = width
        self.window_height = height
        self.rng = random.Random()

    def build_okey_set(self):
        """
        Builds the tiles that are used in the game
        106 total tiles
        Numbers 1-13; 2 copies of each
        2 jokers
        4 colors
        """

        tiles = []
        for color, symbol in TILE_COLORS_SYMBOLS.items():
            for number in range(1, 14):
                # appending two copies of each tile
                tiles.append(Tile(TileInfo(number, color, symbol, 0)))
                tiles.append(Tile(TileInfo(number, color, symbol, 1)))

        # Adding the jokers
        tiles.append(Tile(TileInfo(0, colr.GREEN, "⚡", 0)))
        tiles.append(Tile(TileInfo(0, colr.GREEN, "⚡", 1)))

        return tiles

    # Dealer to set up a new round,
    def deal_new_round(self, players, starting_player_idx = 0):
        if len(players) != 4:
            raise AttributeError('Okey game requires four players.')

        # Build + shuffle
        tiles = self.build_okey_set()
        self.rng.shuffle(tiles)

        # Deal 14 tiles to each player
        for _ in range(14):
            for player in players:
                player.draw_tile(tiles.pop())

        # Starting player is dealt 15 tiles
        players[starting_player_idx].draw_tile(tiles.pop())

        # remaining tiles go on draw pile
        draw_pile = DrawPile(self.window_width / 2,
            self.window_height / 2, tiles)

        # return this draw pile back
        return draw_pile

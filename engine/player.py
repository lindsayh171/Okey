class Player:
    def __init__(self, name, is_player_ai = False): # distinguish human player vs AI player
        self.name = name
        self.is_player_ai = is_player_ai
        self.hand = [] # every player has a hand of tiles, empty initially
        self.discard_pile = [] # player's discard piles, empty initially
        self.opened = False
        self.stars = 0
        self.total_score = 0 # accumulates over the no. of rounds

    def draw_tile(self, tile):
        self.hand.append(tile)

    def discard_tile(self, tile):
        if tile not in self.hand:
            raise ValueError("Tile not in hand to be discarded")
        self.hand.remove(tile)
        self.discard_pile.append(tile)
        return tile # visible face-up tile discarded

    def hand_size(self):
        return len(self.hand)

    # returns the last visible face-up discarded tile of player
    def top_discard(self):
        if len(self.discard_pile) > 0:
            return self.discard_pile[-1]
        else:
            return None









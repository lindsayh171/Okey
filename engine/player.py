from collections import defaultdict

class Player:
    """
    Player class
    Attributes:
        name - screen name
        is_player_ai
        hand - tiles the player has
        player - tiles shown once player opens
        discard_pile - cards this player has discarded
    """
    def __init__(self, disc, name, is_player_ai = False): # distinguish human player vs AI player
        self.name = name
        self.is_player_ai = is_player_ai
        self.hand = [] # every player has a hand of tiles, empty initially
        self.played = [] # tiles that are displayed when the player opens
        self.discard_pile = disc # player's discard piles, empty initially
        self.opened = False
        self.stars = 0
        self.hand_score = 0 #score used for opening
        self.turn_score = 0 # score during a round that is added to total
        self.total_score = 0 # accumulates over the no. of rounds
        self.drawn = False # Keeps track that one tile has been drawn per round

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
        return None

    # Calculates the possible points earned for the player based on their current hand
    def get_hand_score(self):
        # Resets turn_score each time points are calculated
        self.hand_score = 0
        # Create a copy of the player's hand so we don't modify the original list
        score_hand = list(self.hand)

        # Keep track of tiles that have already been used in a set or run
        # This prevents double-counting and enforces set priority
        used_tiles = set()

        # ===================================
        # Check For Sets (Priority Over Runs)
        # A set = 3-4 tiles of the same number, all different colors
        # ===================================

        # Group tiles by number
        # Example: {5: [tile1, tile2, tile3], 8: [tile4, tile5]}
        number_groups = defaultdict(list)

        for tile in score_hand:
            number_groups[tile.value].append(tile)

        # Evaluate each number group to see if it forms a valid set
        for _, tiles in number_groups.items():

            # Only consider tiles that have not already been used
            available_tiles = [t for t in tiles if t not in used_tiles]

            # Ensure colors are unique (sets require different colors)
            # Dictionary prevents duplicate colors
            unique_colors = {}
            for tile in available_tiles:
                if tile.color not in unique_colors:
                    unique_colors[tile.color] = tile

            # Valid set must have 3 or 4 different colors
            if 3 <= len(unique_colors) <= 4:
                valid_set = list(unique_colors.values())

                # Mark these tiles as used so runs cannot reuse them
                for tile in valid_set:
                    used_tiles.add(tile)

                # Add sum of tile numbers to score
                self.hand_score += sum(tile.value for tile in valid_set)

        # ===================================
        # Check For Runs (Using Remaining Tiles Only)
        # A run = 3+ consecutive numbers of the same color
        # ===================================

        # Group remaining (unused) tiles by color
        color_groups = defaultdict(list)

        for tile in score_hand:
            if tile not in used_tiles:
                color_groups[tile.color].append(tile)

        # Check each color group for consecutive sequences
        for _, tiles in color_groups.items():

            # Sort tiles by number to detect consecutive values
            # Ignores Jokers for the time being
            tiles = sorted(
                [t for t in tiles if t.value is not None],
                key=lambda t: t.value
            )

            # Start building a potential run
            current_run = [tiles[0]] if tiles else []

            # Iterate through sorted tiles to detect consecutive numbers
            for i in range(1, len(tiles)):

                # If current tile is exactly 1 greater than previous → consecutive
                if tiles[i].value == tiles[i - 1].value + 1:
                    current_run.append(tiles[i])

                else:
                    # Sequence broke — check if the previous run is valid
                    if len(current_run) >= 3:
                        self.hand_score += sum(t.value for t in current_run)

                        # Mark run tiles as used
                        for t in current_run:
                            used_tiles.add(t)

                    # Start a new potential run
                    current_run = [tiles[i]]

            # After loop ends, check the final run
            if len(current_run) >= 3:
                self.hand_score += sum(t.value for t in current_run)
                for t in current_run:
                    used_tiles.add(t)

        # Return score
        return self.hand_score

    # Calculates the turn score after the turn has ended
    def get_turn_score(self):
        self.hand_score += sum(tile.value for tile in self.hand)
        return self.turn_score

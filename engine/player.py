"""
Player class handles both human and computer players in the game.
Each maintaining a hand of tiles, associated discard pile and current
scores that are dependent on how each evaluates tiles.
"""
from collections import defaultdict
import math


# helper function to measure distance between two tiles
def distance(t1, t2):
    return math.sqrt(
        (t1.center_x - t2.center_x) ** 2 +
        (t1.center_y - t2.center_y) ** 2
    )


# function that finds nearby tiles
def group_tiles(tiles, threshold = 25):
    """
    Go over tiles/hand and create groups from it
    based on their coordinates (distance)
    """

    groups = []
    # to keep track of tiles already grouped
    visited = set()

    for tile in tiles:
        # skipping tiles already part of a group
        if tile in visited:
            continue

        # Build the group once identified
        group = []
        # Begin group search from this tile
        stack = [tile]

        # find all tiles that are close enough
        while stack:
            current = stack.pop()
            if current in visited:
                continue

            # mark tile as used and append to current group
            visited.add(current)
            group.append(current)

            # check other tiles to see if they belong in this group
            for other_t in tiles:
                if other_t not in visited:
                    if distance(current, other_t) < threshold:
                        stack.append(other_t)
                        # Obtain the distance between tiles to set threshold
                        # print("distance:", distance(current, other_t))

        # Append to group object list once group is built
        groups.append(group)

    # once every group is added to the list, return
    return groups


#
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

    # TO-DO: address disabled 'R0902: Too many instance attributes'
    # pylint: disable=R0902

    def __init__(self, disc, name, is_player_ai = False):
        self.name = name
        self.is_player_ai = is_player_ai # distinguish human player vs AI player
        self.hand = [] # every player has a hand of tiles, empty initially
        self.groups = [] # groups of tiles put together by player, empty initially
        self.played = [] # tiles that are displayed when the player opens
        self.sets_played = [] # sets of tiles out of what the player has opened with
        self.discard_pile = disc # player's discard piles, empty initially
        self.opened = False
        self.stars = 0
        self.hand_score = 0 # score used for opening
        self.turn_score = 0 # score during a round that is added to total
        self.total_score = 0 # accumulates over the no. of rounds
        self.drawn = False # Keeps track that one tile has been drawn per round

    def draw_tile(self, tile):
        """
        Function that adds a tile to a player's hand
        """
        self.hand.append(tile)

    def discard_tile(self, tile):
        """
        Removes a tile from the player's hand and
        puts it in the discard pile
        '"""
        if tile not in self.hand:
            raise ValueError("Tile not in hand to be discarded")
        self.hand.remove(tile)
        self.discard_pile.append(tile)
        return tile # visible face-up tile discarded

    def hand_size(self):
        """
        returns number of tiles in the hand
        """
        return len(self.hand)

    def top_discard(self):
        """
        returns the last visible face-up discarded tile of player
        """
        if len(self.discard_pile) > 0:
            return self.discard_pile[-1]
        return None

    # TO-DO: address disabled 'R0912: Too many branches'
    # pylint: disable=R0912
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

    # This function calculates hand_score for player
    # based on physical arrangement/ coordinates
    def player_get_hand_score(self):
        """
        data structure: list of group objects
        Go over tiles/ hand of the user
        Create groups based on coordinates
        Evaluate each group -> set, run
        Calculate each group's score
        Returns summed score from all groups evaluated
        """

        self.hand_score = 0

        # Go over tiles and create groups from it
        self.groups = group_tiles(self.hand)

        ## print("GROUPS:", [[(t.value, t.color) for t in g] for g in self.groups])

        # Once every group is created
        for group in self.groups:

            # skip small groups
            if len(group) < 3:
                continue

            # extract colors and numbers
            colors = []
            numbers = []

            for tile in group:
                colors.append(tile.color)
                numbers.append(tile.value)

            # sort to account for a player's disarranged tiles -> 1, 3, 2
            numbers.sort()

            # -------------------------
            # CHECK SET - tiles of same number, but
            #  different color --> 1(red), 1(blue), 1(black)
            # -------------------------

            # check if all tiles are the same number
            one_number = len(set(numbers)) == 1
            # check that are colors are different
            diff_colors = len(set(colors)) == len(colors)

            if one_number and diff_colors:
                self.hand_score += sum(numbers)
                continue

            # -------------------------
            # CHECK RUN - tiles of same color, but
            # different number --> 1(red), 2(red), 3(red)
            # -------------------------

            # check if all tiles are the same color
            same_color = len(set(colors)) == 1

            # check for consecutive order
            consecutive_order = True
            for i in range(len(numbers) - 1):
                if numbers[i] + 1 != numbers[i + 1]:
                    consecutive_order = False
                    break

            if same_color and consecutive_order:
                self.hand_score += sum(numbers)

        # returns sum group scores of evaluated groups
        return self.hand_score

    # Calculates the turn score after the turn has ended
    def get_turn_score(self):
        self.hand_score += sum(tile.value for tile in self.hand)
        return self.turn_score

# TO-DO: address disabled 'R0903: Too few public methods'
# pylint: disable=R0903
### Testing player_get_hand_score() and group_tiles()
class DummyTile:
    """
    For testing purposes before integrating to GUI
    """
    def __init__(self, x, y, color, value):
        self.center_x = x
        self.center_y = y
        self.color = color
        self.value = value


tile1 = DummyTile(0, 0, "red", 1)
tile2 = DummyTile(19, 0, "red", 2)
tile3 = DummyTile(20, 0, "red", 3)

player = Player(0, "Joe", False)
player.hand = [tile1, tile2, tile3]


print(player.player_get_hand_score())

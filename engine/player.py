"""
Player class handles both human and computer players in the game.
Each maintaining a hand of tiles, associated discard pile and current
scores that are dependent on how each evaluate tiles.
"""

from collections import defaultdict
import math


def distance(t1, t2):
    """
    helper function to measure the Euclidean distance
    between two tiles using their center positions
    (center_x, center_y) on the screen
    """
    return math.sqrt(
        (t1.center_x - t2.center_x) ** 2 +
        (t1.center_y - t2.center_y) ** 2
    )


def group_tiles(tiles, y_threshold = 25):
    """
    Tiles are grouped into rows based on how close they are vertically, Y positions.
    Horizontal spacing (x) is handled later to split rows into actual tile groups.
    """

    # list of lists
    groups = []

    # processing tiles from top to bottom - y position
    sorted_tiles = sorted(tiles, key=lambda t: t.center_y)

    for tile in sorted_tiles:
        placed = False

        # processing one row at a time
        for group in groups:
            # if tile is close enough vertically, it belongs in same row
            if abs(tile.center_y - group[0].center_y) < y_threshold:
                group.append(tile)
                placed = True
                break

        # If tile not placed, create new row starting with this tile
        # inside groups
        if not placed:
            groups.append([tile])

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
        self.locked_score = 0
        self.can_open = False
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
        - Tiles are grouped into rows (Y position)
        - Rows are split into subgroups (based on X spacing)
        - Each subgroup must be valid:
            - SET (same number, different colors) --> 1(red), 1(blue), 1(black)
            - OR RUN (same color, different numbers) -> 1(red), 2(red), 3(red)
        - If a subgroup is invalid, gets 0 points
        """

        # Reset score every time
        self.hand_score = 0

        # to track how many valid groups (sets and runs) are found
        valid_group_count = 0

        # group tiles into rows based on y position
        self.groups = group_tiles(self.hand)

        # Loop through each row
        for group in self.groups:

            # skip empty groups
            if not group:
                continue

            # Sort tiles left → right
            group = sorted(group, key=lambda t: t.center_x)

            # -------------------------
            # Split into subgroups (based on X spacing)
            # -------------------------
            subgroups = []

            # dynamic list that grows and resets
            current_subgroup = [group[0]]

            for i in range(1, len(group)):
                curr = group[i]

                # If gap is large → new subgroup
                if abs(curr.center_x - current_subgroup[-1].center_x) > 100:
                    subgroups.append(current_subgroup)
                    current_subgroup = [curr]
                else:
                    current_subgroup.append(curr)

            # Append the last subgroup
            subgroups.append(current_subgroup)

            # -------------------------
            # Test validity of each subgroup
            # -------------------------
            for subgroup in subgroups:

                # Ignore groups smaller than 3
                if len(subgroup) < 3:
                    continue

                # extract tile values and colors
                numbers = [t.value for t in subgroup]
                colors = [t.color for t in subgroup]


                # -------------------------
                # CHECK SET +
                # Other conditions:
                # - 3 or 4 tiles
                # -------------------------
                same_number = len(set(numbers)) == 1
                all_diff_colors = len(set(colors)) == len(colors)

                if 3 <= len(subgroup) <= 4 and same_number and all_diff_colors:
                    print(f"SET FOUND: {numbers[0]}")
                    self.hand_score += sum(numbers)
                    valid_group_count += 1
                    continue  # don't check run if already a set

                # -------------------------
                # CHECK RUN
                # -------------------------
                same_color = len(set(colors)) == 1

                # Sort numbers to check sequence order
                sorted_numbers = sorted(numbers)

                # Check if each number increases by 1
                is_consecutive = True
                for i in range(len(sorted_numbers) - 1):
                    if sorted_numbers[i] + 1 != sorted_numbers[i + 1]:
                        is_consecutive = False
                        break

                if same_color and is_consecutive:
                    print(f"RUN FOUND: {sorted_numbers}")
                    self.hand_score += sum(sorted_numbers)
                    valid_group_count += 1

        # Debug: show how many valid groups were found
        print("Number of valid groups found:", valid_group_count)

        # Return total score from all valid groups sums
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
    def __repr__(self):
        return f"{self.value}{self.color[0]}({self.center_x},{self.center_y})"



tile1 = DummyTile(0, 0, "red", 1)
tile2 = DummyTile(19, 0, "red", 2)
tile3 = DummyTile(20, 0, "red", 3)

player = Player(0, "Joe", False)
player.hand = [tile1, tile2, tile3]


# print(player.player_get_hand_score())

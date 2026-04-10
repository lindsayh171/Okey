"""
Player class handles both human and computer players in the game.
Each maintaining a hand of tiles, associated discard pile and current
scores that are dependent on how each evaluate tiles.
"""

from collections import defaultdict
import math
from board_components.open_stand import OpenStand

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

    def __init__(self, disc, name, is_player_ai = False):
        self.name = name
        self.is_player_ai = is_player_ai # distinguish human player vs AI player
        self.hand = [] # every player has a hand of tiles, empty initially
        self.played = [] # tiles that are displayed when the player opens
        self.open_tiles = [[],[],[],[]] # sets of tiles out of what the player has opened with
        self.arranged_groups = [] # to track player's list of arranged valid groups
        self.open_stand = OpenStand(self)
        self.used_tiles = set()  # Keep track of tiles that have already been used in a set or run
        self.discard_pile = disc # player's discard piles, empty initially
        self.opened = False
        self.opened_this_turn = False # to prevent player from expanding tiles during opening
        self.stars = 0
        self.hand_score = 0 # score used for opening
        self.turn_score = 0 # score during a round that is added to total
        self.round_scores = [] # scores of each turn
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

    def com_discard_tile(self):
        """Handles AI player's discard logic."""
        if self.opened:

            valid_tiles = [t for t in self.hand if t is not None]

            if not valid_tiles:
                return None

            highest_tile = max(valid_tiles, key=lambda t: t.tile_info.value)

            self.hand.remove(highest_tile)

            return highest_tile
        # Filter tiles that:
        # - are not None
        # - were not used in scoring
        candidates = [
            tile for tile in self.hand
            if tile is not None and tile not in self.used_tiles
        ]

        # If no valid tiles to discard, do nothing
        if not candidates:
            return None

        # Find the tile with the lowest value
        lowest_tile = min(candidates, key=lambda t: t.tile_info.value)

        # Remove it from hand and add to discard
        self.hand.remove(lowest_tile)

        return lowest_tile

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
        """Scores hand, sorts self.hand into sets/runs,
        and stores only valid sets/runs in used_tiles"""

        # Resets score each time points are calculated
        self.hand_score = 0

        # Stores grouped sets/runs for ordering self.hand
        final_groups = []

        # used_tiles ONLY contains valid sets/runs (no leftovers)
        self.used_tiles = []

        # ===================================
        # Check For Sets (Priority Over Runs)
        # A set = 3-4 tiles of the same number, all different colors
        # ===================================

        number_groups = defaultdict(list)

        for tile in self.hand:
            if tile is None:
                continue  # IMPORTANT: skip separators

            number_groups[tile.tile_info.value].append(tile)

        for _, tiles in number_groups.items():

            available_tiles = [t for t in tiles if t not in self.used_tiles]

            unique_colors = {}
            for t in available_tiles:
                if t.tile_info.color not in unique_colors:
                    unique_colors[t.tile_info.color] = t

            if 3 <= len(unique_colors) <= 4:
                valid_set = list(unique_colors.values())

                final_groups.append(valid_set)

                # Store into used_tiles with separator
                self.used_tiles.extend(valid_set)
                self.used_tiles.append(None)

                for t in valid_set:
                    self.hand_score += t.tile_info.value

        # ===================================
        # Check For Runs (Using Remaining Tiles Only)
        # A run = 3+ consecutive numbers of the same color
        # ===================================

        color_groups = defaultdict(list)

        for tile in self.hand:
            if tile is None:
                continue  # skip separators

            if tile not in self.used_tiles:
                color_groups[tile.tile_info.color].append(tile)

        for _, tiles in color_groups.items():
            tiles = sorted(
                [t for t in tiles if t.tile_info.value is not None],
                key=lambda t: t.tile_info.value
            )

            i = 0
            while i < len(tiles):
                run = [tiles[i]]
                for j in range(i + 1, len(tiles)):
                    if tiles[j].tile_info.value == run[-1].tile_info.value + 1:
                        run.append(tiles[j])
                    else:
                        break

                if len(run) >= 3:
                    final_groups.append(run)
                    self.used_tiles.extend(run)
                    self.used_tiles.append(None)
                    for t in run:
                        self.hand_score += t.tile_info.value
                    i += len(run)
                else:
                    i += 1

        # ===================================
        # Collect Leftover Tiles (Not part of any set/run)
        # ===================================

        leftovers = [t for t in self.hand if t is not None and t not in self.used_tiles]

        # ===================================
        # Sort the Hand (Sets/Runs First, Leftovers Last)
        # ===================================

        self.hand = []

        # Add each valid group with None separators
        for group in final_groups:
            self.hand.extend(group)
            self.hand.append(None)

        # Add leftover tiles at the end (no separator after)
        self.hand.extend(leftovers)

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
        self.arranged_groups = []

        # Loop through each row
        for group in group_tiles(self.hand):
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

            for tile in group[1:]:
                # If gap is large → new subgroup
                if abs(tile.center_x - current_subgroup[-1].center_x) > 100:
                    subgroups.append(current_subgroup)
                    current_subgroup = [tile]
                else:
                    current_subgroup.append(tile)

            # Append the last subgroup
            subgroups.append(current_subgroup)

            # -------------------------
            # Test validity of each subgroup
            # -------------------------
            for subgroup in subgroups:

                # Ignore groups smaller that are not 3-4 tiles
                if len(subgroup) < 3: #or len(subgroup) > 4
                    continue

                # check regular and joker tiles
                joker_tiles = [t for t in subgroup if t.tile_info.value == 0]
                normal_tiles = [t for t in subgroup if t.tile_info.value != 0]

                # extract tile values and colors
                numbers = [t.tile_info.value for t in normal_tiles]
                colors = [t.tile_info.color for t in normal_tiles]


                # -------------------------
                # CHECK SET
                # -------------------------
                same_number = len(set(numbers)) == 1
                all_diff_colors = len(set(colors)) == len(colors)

                if 3 <= len(subgroup) <= 4 and same_number and all_diff_colors:
                    self.hand_score += sum(numbers)

                    # add the jokers to the score
                    self.hand_score += numbers[0] * len(joker_tiles)

                    self.arranged_groups.append(subgroup)

                    continue  # don't check run if already a set


                # -------------------------
                # CHECK RUN
                # -------------------------
                same_color = len(set(colors)) == 1

                # Check if each number increases by 1
                is_consecutive = True
                all_values = [t.tile_info.value for t in subgroup]
                # set joker values
                for index, _ in enumerate(all_values):
                    # make joker value the next consecutive value if prior tile is valid
                    if all_values[index] == 0 and index > 0:
                        # joker cannot be 14
                        if all_values[index - 1] == 13:
                            is_consecutive = False
                            break
                        all_values[index] = all_values[index - 1] + 1
                    # check if first tile is joker
                    elif all_values[index] == 0 and index == 0:
                        # joker cannot come before a 1 (or two jokers before a two)
                        if all_values[index + 1] == 1 or all_values[index + 2] == 2:
                            is_consecutive = False
                            break
                        # check for two jokers in a row
                        if all_values[index + 1] == 0:
                            all_values[index] = all_values[index + 2] - 2
                        else:
                            all_values[index] = all_values[index + 1] - 1

                # check normal tiles
                for index in range(len(all_values) - 1):
                    if all_values[index] + 1 != all_values[index + 1]:
                        is_consecutive = False
                        break

                # check color and add to hand score
                if same_color and is_consecutive:
                    self.hand_score += sum(all_values)

                    self.arranged_groups.append(subgroup)

        # Return total score from all valid groups sums
        return self.hand_score

    # Calculates the turn score after the turn has ended
    def get_turn_score(self):
        """Calculates the turn score after the turn has ended"""
        self.turn_score += sum(tile.tile_info.value for tile in self.hand)
        return self.turn_score

    def open(self):
        """Populates open_tiles from used_tiles and removes tiles from hand"""
        print(f"*** {self.name} opened ***")
        self.opened = True
        self.open_tiles = []
        current_group = []

        for tile in self.used_tiles:

            if tile is None:
                if current_group:
                    self.open_tiles.append(current_group)
                    current_group = []
            else:
                current_group.append(tile)

                if tile in self.hand:
                    self.hand.remove(tile)

        # append last group if exists
        if current_group:
            self.open_tiles.append(current_group)

    def add_valid_tiles_to_open(self):
        """
        1. Uses get_hand_score() to generate full sets/runs in used_tiles
        2. Moves those groups into open_tiles
        3. Then tries to add remaining single tiles from hand into existing groups
        """

        # ---------------------------------------------------
        # STEP 1: Generate valid sets/runs (stored in used_tiles)
        # ---------------------------------------------------
        self.get_hand_score()

        # ---------------------------------------------------
        # STEP 2: Move full groups from used_tiles → open_tiles
        # ---------------------------------------------------
        new_groups = []
        current = []

        for tile in self.used_tiles:
            # None acts as a separator between groups inside used_tiles
            # (if present). We finalize the current group when we hit it.
            if tile is None:
                if current:
                    new_groups.append(current)
                    current = []
            else:
                # Build the current run/set group
                current.append(tile)

        # Append the last group if the list did not end with None
        if current:
            new_groups.append(current)

        for group in new_groups:
            # Each group is independent and must NEVER merge with
            # existing groups in open_tiles
            self.open_tiles.append(group)

            # Remove committed tiles from hand so they cannot be reused
            # in future scoring cycles
            for tile in group:
                if tile in self.hand:
                    self.hand.remove(tile)

        # ---------------------------------------------------
        # STEP 3: Try to add leftover single tiles into groups
        # ---------------------------------------------------
        for tile in self.hand[:]:

            if tile is None:
                continue
            for group in self.open_tiles:
                if not group:
                    continue

                if group[0] is None:
                    continue

                # extra safety: strip any accidental None holdover
                group = [t for t in group if t is not None]
                if not group:
                    continue

                # -------------------------
                # CHECK IF GROUP IS A SET
                # -------------------------
                is_set = all(t.tile_info.value == group[0].tile_info.value for t in group)

                if is_set:
                    # Must match value
                    if tile.tile_info.value != group[0].tile_info.value :
                        continue

                    # Enforce unique colors in set
                    colors = {t.tile_info.color for t in group}
                    if tile.tile_info.color in colors:
                        continue

                    group.append(tile)
                    self.hand.remove(tile)
                    break

                # -------------------------
                # CHECK IF GROUP IS A RUN
                # -------------------------
                is_run = all(t.tile_info.color == group[0].tile_info.color for t in group)

                if is_run:
                    if tile.tile_info.color != group[0].tile_info.color:
                        continue

                    values = sorted(t.tile_info.value for t in group)

                    # Add to front
                    if tile.tile_info.value == values[0] - 1:
                        group.insert(0, tile)
                        self.hand.remove(tile)
                        break

                    # Add to back
                    if tile.tile_info.value == values[-1] + 1:
                        group.append(tile)
                        self.hand.remove(tile)
                        break

    def print_open_tiles(self):
        """Prints open_tiles with visible grouping (sets/runs separated)."""

        print("\nOPEN TILES:")

        for i, group in enumerate(self.open_tiles):

            if not group:
                print(f"Group {i + 1}: EMPTY")
                continue

            values = []

            for tile in group:
                if tile is None:
                    continue  # safety if separators exist

                values.append(tile.tile_info.value)

            print(f"Group {i + 1}: {values}")

    def check_complete(self):
        hand_tiles = [t for t in self.hand if t is not None]
        return len(hand_tiles) == 0

    def check_open(self, open_score):
        if self.hand_score > open_score:
            return True
        return False

    def calculate_round_score(self):
        # player gets 100 points if they did not open
        if not self.opened:
            self.round_scores.append(100)
        else:
            # otherwise calculate the total of tiles still in their hand
            score = 0
            for tile in self.hand:
                score += tile.tile_info.value
            self.round_scores.append(score)

        # add to total score
        self.total_score += self.round_scores[-1]

    def reset(self):
        self.hand = []
        self.played = []  # tiles that are displayed when the player opens
        self.open_tiles = [[], [], [], []]  # sets of tiles out of what the player has opened with
        self.arranged_groups = []  # to track player's list of arranged valid groups
        self.used_tiles = set()  # Keep track of tiles that have already been used in a set or run
        self.opened = False
        self.opened_this_turn = False  # to prevent player from expanding tiles during opening
        self.stars = 0
        self.hand_score = 0  # score used for opening
        self.turn_score = 0  # score during a round that is added to total
        self.drawn = False  # Keeps track that one tile has been drawn per round

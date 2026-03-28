# pylint: disable=too-few-public-methods

# Board class will contain information about a round of Okey, including
# players, the draw pile (middle pile), the last discard tile, and
# other round-relevant data.
# Attempting to make this class act as a centralized source of truth,
# for GUI and engine logic to operate on and remain in sync.

MIN_OPEN = 81
class Board:
    """
    Stores information about a round
    """
    def __init__(self, players, draw_pile, starting_player_idx = 0):
        self.players = players
        self.draw_pile = draw_pile
        self.starting_player_idx = starting_player_idx
        self.curr_player_idx = starting_player_idx # at start, current player is the starting player
        self.last_discard = None # at start, no previous discard yet
        #Minimum value needed to open
        self.min_open = MIN_OPEN # starts at 81 and is increased each time a player opens

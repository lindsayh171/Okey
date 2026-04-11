from enum import Enum

class Views(Enum):
    """Keep track of current view for backtracking"""
    MENU = 'm'
    TITLE = 't'
    END = 'e'
    GAME = 'g'

ROUNDS = 6 # change to 1 to debug

# make initial open 80 because player hand must be strictly greater than open score
INITIAL_OPEN = 80

STARS_OPEN = 100

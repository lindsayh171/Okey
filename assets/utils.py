from enum import Enum

class Views(Enum):
    """Keep track of current view for backtracking"""
    MENU = 'm'
    TITLE = 't'
    END = 'e'
    GAME = 'g'

ROUNDS = 6 # change to 1 to debug
INITIAL_OPEN = 10 # to test for now
STARS_OPEN = 10

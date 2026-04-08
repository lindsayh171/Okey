from enum import Enum

class Views(Enum):
    """Keep track of current view for backtracking"""
    MENU = 'm'
    TITLE = 't'
    END = 'e'

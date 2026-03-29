# This is the face down draw pile (middle pile)

class DrawPile:
    """
    Pile of cards left to draw
    """
    def __init__(self, tiles=None):
        # avoids multiple objects from sharing same list in memory
        if tiles is None:
            self.tiles = []
        else:
            self.tiles = tiles

    def count(self):
        return len(self.tiles)

    def draw(self):
        if len(self.tiles) == 0:
            raise ValueError("DrawPile.draw() called without tiles")
        # for every call, one tile is drawn out
        return self.tiles.pop()

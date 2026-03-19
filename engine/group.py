"""
Evaluates 'groups' formed by tiles put together by the player testing them against rules
"""
class Group:
    TYPE1 = "type1" # run - same color, different number (consecutive)
    TYPE2 = "type2" # set - different color, same number (grouping)
    TYPE3 = "type3" # invalid - gets 0 points
    def __init__(self, tiles):
        self.tiles = tiles
        self.type = None
        self.points = 0

        self.evaluate()

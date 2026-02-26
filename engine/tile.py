# Minimal Tile class

class Tile:
    colors = ("red", "blue", "black", "orange")
    suits = ("circle, triangle, square, star")
    def __init__(self, color, number, suit, is_joker=False, copy_id = 0):
        self.color = color
        self.number = number #Numbers are 1 to 13
        self.suit = suit
        self.is_joker = is_joker
        self.copy_id = copy_id  # two copies of each # tile - this distinguishes duplicate tiles

    def __repr__(self):
        if self.is_joker:
            return "JOKER"
        # for printing clearly
        return f"{self.color}-{self.suits}-{self.number}({self.copy_id}) of 2 copy" 
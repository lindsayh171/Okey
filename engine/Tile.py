# Minimal Tile class

COLORS = ("red", "blue", "black", "orange")

class Tile:
    def __init__(self, color, number, is_joker=False, copy_id = 0):
        self.color = color
        self.number = number
        self.is_joker = is_joker
        self.copy_id = copy_id  # two copies of each # tile - this distinguishes duplicate tiles


    def __repr__(self):
        if self.is_joker:
            return "JOKER"
        return f"{self.color}-{self.number}({self.copy_id}) of 2 copy" # for printing clearly
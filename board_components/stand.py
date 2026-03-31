import arcade
from engine.tile import TILE_WIDTH, TILE_HEIGHT
from board_components.stand_slot import StandSlot, DIVIDER_GAP

class Stand:
    """
    Stand that has stand_slots drawn on top
    """
    def __init__(self):
        self.stand_start_x = 0
        self.stand_divider = 5
        self.rows = 2
        self.columns = 12
        self.total_stand_height = self.rows * TILE_HEIGHT + self.stand_divider
        self.total_stand_width = self.columns * TILE_WIDTH

    def setup(self, screen_width):
        slots_list = []

        # Coordinates of the stand based on the size of the screen
        self.stand_start_x = (screen_width - self.total_stand_width) / 2 + TILE_WIDTH / 2

        # 2 rows in the tile stand
        for row in range(self.rows):
            stand_y = (TILE_HEIGHT / 2) + row * (TILE_HEIGHT + DIVIDER_GAP)
            # 12 slots on each row
            for column in range(self.columns):
                # stand_slot position
                stand_x = self.stand_start_x + column * TILE_WIDTH

                # create stand_slot and append to the slot list
                stand_slot = StandSlot(stand_x, stand_y, arcade.color.BEAVER)
                slots_list.append(stand_slot)

        return slots_list

    def draw(self, slot_list):
        for slot in slot_list:
            slot.draw()

        # draw stand line divider
        arcade.draw_lbwh_rectangle_filled(
            self.stand_start_x - TILE_WIDTH / 2,
            (TILE_HEIGHT + DIVIDER_GAP / 2) - self.stand_divider / 2,
            self.total_stand_width,
            self.stand_divider,
            arcade.color.DEEP_COFFEE,
        )

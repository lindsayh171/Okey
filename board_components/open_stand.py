import arcade

from engine.tile import TILE_WIDTH, TILE_HEIGHT
from board_components.stand_slot import StandSlot, DIVIDER_GAP
from board_components.com import COM_WIDTH
from board_components.stand import Stand

class OpenStand(Stand):
    """
    Open stand with slots and tiles drawn on top
    """
    def __init__(self, player):
        super().__init__()
        self.slots = []
        self.tiles = []
        self.open_stand_start_x = 0
        self.player = player

        self.update()

    def draw_stand(self, screen_width, screen_height):
        # draw window
        arcade.draw_lbwh_rectangle_filled(
            2 * COM_WIDTH + DIVIDER_GAP,
            self.total_stand_height + DIVIDER_GAP,
            screen_width - (4 * COM_WIDTH + 2 * DIVIDER_GAP),
            (screen_height - self.total_stand_height -
             2 * COM_WIDTH - 2 * DIVIDER_GAP),
            arcade.color.GRAY_BLUE
        )

        for slot in self.slots:
            slot.draw()

        for tile in self.tiles:
            tile.draw()

    def update(self):
        self.slots = []
        self.tiles = []

        self.open_stand_start_x = 2 * COM_WIDTH + DIVIDER_GAP + TILE_WIDTH / 2

        start_y = self.total_stand_height + TILE_HEIGHT / 2 + DIVIDER_GAP

        # Build as many rows as the player has sets in their open
        for set_index, current_set in enumerate(self.player.open_tiles):
            # if not isinstance(current_set, list):
            #     continue
            stand_y = start_y + set_index * (TILE_HEIGHT + 2 * DIVIDER_GAP)

            # 1 empty slot on either side of current set
            stand_x = self.open_stand_start_x
            stand_slot = StandSlot(stand_x, stand_y, arcade.color.BLUE)
            stand_slot.holding_tile = False
            stand_slot.open_row_index = set_index
            self.slots.append(stand_slot)

            # current set of tiles and their slots
            for index, tile in enumerate(current_set):
                # set up slots
                stand_x = self.open_stand_start_x + (index + 1) * TILE_WIDTH
                stand_slot = StandSlot(stand_x, stand_y, arcade.color.BLUE)
                stand_slot.holding_tile = True
                stand_slot.open_row_index = set_index
                self.slots.append(stand_slot)

                tile.set_x(self.open_stand_start_x + (index + 1) * TILE_WIDTH)
                tile.set_y(stand_y)
                tile.current_slot = stand_slot
                tile.tile_info.set_face_up()
                self.tiles.append(tile)

            stand_x = self.open_stand_start_x + (len(current_set) + 1) * TILE_WIDTH
            stand_slot = StandSlot(stand_x, stand_y, arcade.color.BLUE)
            stand_slot.holding_tile = False
            stand_slot.open_row_index = set_index
            self.slots.append(stand_slot)

        print(self.tiles)

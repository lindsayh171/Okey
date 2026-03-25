import arcade
import ui_components.rounded_rectangle as rr

from assets.textures import TILE_TEXTURE

TILE_WIDTH = 60
TILE_HEIGHT = 100
TILE_COLORS_SYMBOLS = {arcade.color.RED: "♥", arcade.color.BLACK: "■",
                       arcade.color.BLUE: "●", arcade.color.ORANGE: "▲"}

class Tile(arcade.Sprite):
    """
    Holds all information about an individual tile
    """
    def __init__(self, x, y, value, color, suit, is_joker=False, copy_id = 0, curr_slot = None):
        super().__init__(hit_box_algorithm="None")

        self.value = value
        self.is_face_up = False
        self.color = tuple(color)
        self.suit = suit
        self.is_joker = is_joker
        self.copy_id = copy_id  # two copies of each # tile - this distinguishes duplicate tiles
        self.current_slot = curr_slot
        self.is_in_set = False # distinguish what tiles are in another players set

        self.texture = TILE_TEXTURE

        self.center_x = x
        self.center_y = y

        self.tile_bg = rr.RoundedRectangle(self.center_x - TILE_WIDTH / 2,
            self.center_y - TILE_HEIGHT / 2,
            TILE_WIDTH,
            TILE_HEIGHT,
            TILE_HEIGHT // 4,
      (222, 212, 193)
          )

        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT

        # text for tile
        self.tile_value = arcade.Text(
            str(self.value),
            self.center_x,
            self.center_y + (TILE_HEIGHT / 5),
            self.color,
            40,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # symbol for tile
        self.tile_symbol = arcade.Text(
            str(self.suit),
            self.center_x,
            self.center_y - (TILE_HEIGHT / 3.5),
            self.color,
            15,
            anchor_x="center",
            anchor_y="center"
        )

        # create rectangle
        self.tile_bg = rr.RoundedRectangle(
            self.center_x,
            self.center_y,
            TILE_WIDTH,
            TILE_HEIGHT,
            TILE_HEIGHT // 9,
            (222, 212, 193)
        )

    def draw(self):
        # Rectangle
        self.tile_bg.center_x = self.center_x
        self.tile_bg.center_y = self.center_y
        self.tile_bg.draw()

        # draw value and symbol if face up
        if self.is_face_up:
            # update text and tile positions
            # Update text position to follow tile
            self.tile_value.x = self.center_x
            self.tile_value.y = self.center_y + (TILE_HEIGHT / 5)

            self.tile_symbol.x = self.center_x
            self.tile_symbol.y = self.center_y - (TILE_HEIGHT / 3.5)

            # Value
            self.tile_value.draw()

            # Symbol
            self.tile_symbol.draw()

    def set_face_down(self):
        """ Turn card face-down """
        self.is_face_up = False

    def set_face_up(self):
        """ Turn card face-up """
        self.is_face_up = True

    def get_face_up(self):
        return self.is_face_up

    def set_x(self, val):
        self.center_x = val

    def set_y(self, val):
        self.center_y = val

    def set_curr_slot(self, slot):
        self.current_slot = slot
        self.center_x = slot.center_x
        self.center_y = slot.center_y
        # self.update_position()

    def update_position(self):
        """Update rectangle and text positions to match center_x/center_y"""
        self.tile_bg.center_x = self.center_x
        self.tile_bg.center_y = self.center_y

        self.tile_value.x = self.center_x
        self.tile_value.y = self.center_y + (TILE_HEIGHT / 5)

        self.tile_symbol.x = self.center_x
        self.tile_symbol.y = self.center_y - (TILE_HEIGHT / 3.5)

    def __repr__(self):
        if self.is_joker:
            return "JOKER"
        # for printing clearly
        return f"{self.color}-{self.suit}-{self.value}({self.copy_id}) of 2 copy"

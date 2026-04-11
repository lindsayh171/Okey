import arcade
import ui_components.rounded_rectangle as rr
import assets.colors as colr


TILE_WIDTH = 60
TILE_HEIGHT = 100
TILE_COLORS_SYMBOLS = {colr.RED: "♥", colr.BLACK: "■",
                       colr.BLUE: "●", colr.ORANGE: "▲"}

class TileInfo:
    """
    Helper class to store general information about a tile
    """
    def __init__(self, value, color, suit, copy_id = 0):
        self.value = value
        self.color = color
        self.suit = suit
        self.copy_id = copy_id
        self.is_face_up = False

        # check if joker
        if value == 0:
            self.is_joker = True
        else:
            self.is_joker = False

    def set_face_down(self):
        """ Turn card face-down """
        self.is_face_up = False

    def set_face_up(self):
        """ Turn card face-up """
        self.is_face_up = True

    def get_face_up(self):
        return self.is_face_up

class Tile(arcade.Sprite):
    """
    Holds all information about an individual tile
    """
    def __init__(self, t_info, curr_slot = None):
        super().__init__(hit_box_algorithm="None")

        self.tile_info = t_info
        self.current_slot = curr_slot
        self.is_in_open = False # tile is committed to the open space area

        # text for tile
        if self.tile_info.is_joker:
            tile_value = arcade.Text(
                "〠",
                self.center_x,
                self.center_y + (TILE_HEIGHT / 5),
                self.tile_info.color,
                40,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
        else:
            tile_value = arcade.Text(
                str(self.tile_info.value),
                self.center_x,
                self.center_y + (TILE_HEIGHT / 5),
                self.tile_info.color,
                40,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

        self.gui = {
            "bg": rr.RoundedRectangle(
                [self.center_x, self.center_y],
                [TILE_WIDTH, TILE_HEIGHT],
                TILE_HEIGHT // 9,
                (222, 212, 193)
            ),
            "value": tile_value,
            "symbol": arcade.Text(
                str(self.tile_info.suit),
                self.center_x,
                self.center_y - (TILE_HEIGHT / 3.5),
                self.tile_info.color,
                15,
                anchor_x="center",
                anchor_y="center"
            )
        }

    def draw(self):
        # Rectangle
        self.gui["bg"].center_x = self.center_x
        self.gui["bg"].center_y = self.center_y
        self.gui["bg"].draw()

        # draw value and symbol if face up
        if self.tile_info.get_face_up():
            # update text and tile positions
            # Update text position to follow tile
            self.gui["value"].x = self.center_x
            self.gui["value"].y = self.center_y + (TILE_HEIGHT / 5)

            self.gui["symbol"].x = self.center_x
            self.gui["symbol"].y = self.center_y - (TILE_HEIGHT / 3.5)

            # Value
            self.gui["value"].draw()

            # Symbol
            self.gui["symbol"].draw()

    def set_x(self, val):
        self.center_x = val

    def set_y(self, val):
        self.center_y = val

    def set_curr_slot(self, slot):
        self.current_slot = slot
        self.center_x = slot.center_x
        self.center_y = slot.center_y

    def highlight(self):
        self.gui["bg"].color = colr.LIGHT_GOLDENROD_YELLOW

    def unhighlight(self):
        self.gui["bg"].color = (222, 212, 193)

    def tile_clicked(self, x, y):
        """
        Check whether tile was clicked (bounds match centered TILE_WIDTH × TILE_HEIGHT)
        """
        half_w = TILE_WIDTH / 2
        half_h = TILE_HEIGHT / 2
        return (
            self.center_x - half_w < x < self.center_x + half_w
            and self.center_y - half_h < y < self.center_y + half_h
        )

    def __repr__(self):
        if self.tile_info.is_joker:
            return "JOKER"
        # for printing clearly
        return (f"{self.color}-{self.tile_info.suit}-{self.tile_info.value}"
                f"({self.tile_info.copy_id}) of 2 copy")

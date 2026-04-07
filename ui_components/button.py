import arcade
from ui_components import rounded_rectangle

class Button:
    """
    Creates a button using a rounded rectangle and text.
    """
    def __init__(self, coords, dimensions, value, colors):
        self.coordinates = {"x": coords[0], "y": coords[1]}
        self.dimensions = {"width": dimensions[0], "height": dimensions[1]}
        self.text = value
        self.radius = self.dimensions["height"] // 4

        self.colors = {"color": colors[0],
                       "text_color": colors[1]}

        self.rect = rounded_rectangle.RoundedRectangle(
            [self.coordinates["x"], self.coordinates["y"]],
            [self.dimensions["width"], self.dimensions["height"]],
            self.radius,
            self.colors["color"],
        )
        self.label = arcade.Text(
            self.text,
            self.coordinates["x"],
            self.coordinates["y"] - self.dimensions["height"] // 4,
            self.colors["text_color"],
            font_size = self.dimensions["height"] * 0.6,
            anchor_x="center",
            font_name="Itim"
        )

    def draw(self):
        self.rect.draw()
        self.label.draw()

    def button_pressed(self, x, y):
        """
        Checks if the button collides with the point pressed

        :param x: x coordinate
        :param y: y coordinate
        :return: true if collides, false otherwise
        """
        return self.rect.collided_with_rect(x, y)

    def set_color(self, color):
        self.colors["color"] = color
        self.rect.color = color

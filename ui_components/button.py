import arcade
from ui_components import rounded_rectangle
import assets.sounds as sounds
from assets.sounds import VOLUME

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
        if self.rect.collided_with_rect(x, y):
            # Sound effect
            arcade.play_sound(sounds.button, VOLUME)
            return self.rect.collided_with_rect(x, y)

        return self.rect.collided_with_rect(x, y)

    def set_color(self, color):
        self.colors["color"] = color
        self.rect.color = color

    def show_pressed_button(self, pressed_color):
        """
        Shows button has been pressed and goes back to original color afterwards.
        :return: NULL
        """
        original_color = self.colors["color"]

        self.set_color(pressed_color)

        # sets color back to original after a second
        def reset_color(dt):
            self.set_color(original_color)

        # Change the color for a split second to look like it was pressed
        arcade.schedule_once(reset_color, 0.1)

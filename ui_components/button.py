import arcade
import ui_components.rounded_rectangle as rounded_rectangle

class Button():
    def __init__(self, x, y, width, height, value, color, text_color):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.text = value
        self.radius = height // 4

        self.color = color
        self.text_color = text_color
        self.hover_color = arcade.color.SPRING_GREEN
        self.current_color = self.color

        self.label = arcade.Text(
            self.text,
            self.center_x,
            self.center_y - self.height // 4,
            self.text_color,
            font_size= self.height * 0.6,
            anchor_x="center",
            font_name="Itim"
        )

        # draw a rounded rectangle
        self.rect = rounded_rectangle.RoundedRectangle(self.center_x,
                                                  self.center_y,
                                                  self.width,
                                                  self.height,
                                                  self.radius,
                                                  self.color)

    def draw(self):

        # draw button text
        arcade.load_font("../assets/fonts/Itim-Regular.ttf")

        self.rect.draw()
        self.label.draw()
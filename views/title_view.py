import arcade
import ui_components.button as button

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = (1, 22, 56)

        arcade.load_font("../assets/fonts/IrishGrover-Regular.ttf")

        title_x = self.window.width / 2
        title_y = self.window.height / 2

        self.title_text = arcade.Text(
            "Okey",
            title_x,
            title_y,
            (255, 107, 107),
            font_size= self.window.height * 0.3,
            anchor_x="center",
            font_name="Irish Grover"
        )

        button_width = self.window.width / 5
        button_height = self.window.height / 10

        self.play_button = button.Button(title_x - button_width * 0.8,
                             title_y - button_height * 1.6,
                             button_width,
                             button_height,
                             "Play",
                             (255, 230, 109),
                             (1, 22, 56))

        self.rules_button = button.Button(title_x + button_width * 0.8,
                                          title_y - button_height * 1.6,
                                          button_width,
                                          button_height,
                                          "Rules",
                                          (78, 205, 196),
                                          (1, 22, 56))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.title_text.draw()
        self.play_button.draw()
        self.rules_button.draw()

def main():
    """ Main function """
    window = arcade.Window(1000, 800, "Okey")
    start_view = TitleView()
    window.show_view(start_view)
    arcade.run()

if __name__ == '__main__':
    main()


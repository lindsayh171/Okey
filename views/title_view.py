import arcade

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = (1, 22, 56)

        self.title_text = arcade.Text("Okey", self.window.width / 2, self.window.height / 2,
                                      (255, 107, 107), font_size=50, anchor_x="center")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.title_text.draw()
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

def main():
    """ Main function """
    window = arcade.Window(1000, 800, "Okey")
    start_view = TitleView()
    window.show_view(start_view)
    arcade.run()

if __name__ == '__main__':
    main()


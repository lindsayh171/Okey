import arcade
from ui_components import button
from views.name_view import NameView
from views.rules_view import RulesView
import assets.colors as colr
from assets.utils import Views

class TitleView(arcade.View):
    """
    Start screen of game with "Play" and "Rules" options
    """
    def __init__(self):
        super().__init__()

        self.title_text = None
        self.play_button = None
        self.rules_button = None

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = colr.THEME_DARK_BLUE

        title_x = self.window.width / 2
        title_y = self.window.height / 2

        button_width = self.window.width / 5
        button_height = self.window.height / 10

        arcade.load_font("assets/fonts/IrishGrover-Regular.ttf")

        # title text
        self.title_text = arcade.Text(
            "Okey",
            title_x,
            title_y,
            colr.THEME_PINK,
            font_size=self.window.height * 0.3,
            anchor_x="center",
            font_name="Irish Grover"
        )

        # play button
        self.play_button = button.Button(title_x - button_width * 0.8,
                                         title_y - button_height * 1.6,
                                         button_width,
                                         button_height,
                                         "Play",
                                         colr.THEME_YELLOW,
                                         colr.THEME_DARK_BLUE)

        # rules button
        self.rules_button = button.Button(title_x + button_width * 0.8,
                                          title_y - button_height * 1.6,
                                          button_width,
                                          button_height,
                                          "Rules",
                                          colr.THEME_TEAL,
                                          colr.THEME_DARK_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.title_text.draw()
        self.play_button.draw()
        self.rules_button.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        if self.play_button.button_pressed(x,y):
            name_view = NameView()
            self.window.show_view(name_view)
        if self.rules_button.button_pressed(x, y):
            rules_view = RulesView(Views.TITLE)
            self.window.show_view(rules_view)

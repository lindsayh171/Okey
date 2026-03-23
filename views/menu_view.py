import arcade
from ui_components import button
import assets.colors as colr
from assets.utils import Views

class MenuView(arcade.View):
    """
    Start screen of game with "Play" and "Rules" options
    """

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.title_text = None
        self.close_button = None
        self.quit_button = None
        self.rules_button = None

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = colr.THEME_LIGHT_BLUE

        title_x = self.window.width / 2
        title_y = 6 * self.window.height / 10

        button_width = self.window.width / 6
        button_height = self.window.height / 12
        close_button = self.window.height / 16

        arcade.load_font("assets/fonts/IrishGrover-Regular.ttf")

        # title text
        self.title_text = arcade.Text(
            "Menu",
            title_x,
            title_y,
            colr.THEME_PINK,
            font_size=self.window.height * 0.1,
            anchor_x="center",
            font_name="Irish Grover"
        )

        # close button
        self.close_button = button.Button(title_x + close_button * 3,
                                         title_y + close_button * 1.5,
                                         close_button,
                                         close_button,
                                         "❌",
                                         colr.THEME_LIGHT_BLUE,
                                         colr.THEME_DARK_BLUE)

        # rules button
        self.rules_button = button.Button(title_x,
                                          title_y - button_height * 1.2,
                                          button_width,
                                          button_height,
                                          "Rules",
                                          colr.THEME_TEAL,
                                          colr.THEME_DARK_BLUE)

        self.quit_button = button.Button(title_x,
                                          title_y - button_height * 3,
                                          button_width,
                                          button_height,
                                          "Quit",
                                          colr.THEME_YELLOW,
                                          colr.THEME_DARK_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.title_text.draw()
        self.close_button.draw()
        self.rules_button.draw()
        self.quit_button.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.close_button.button_pressed(x, y):
            self.window.show_view(self.game_view)
        if self.rules_button.button_pressed(x, y):
            from views.rules_view import RulesView

            rules_view = RulesView(Views.MENU, self.game_view)
            self.window.show_view(rules_view)
        if self.quit_button.button_pressed(x, y):
            self.window.show_view(self.window.title_view)

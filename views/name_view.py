import arcade
import arcade.gui as gui
import assets.colors as colr
import ui_components.button as button
from views.game_view import GameView

class NameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        self.manager.enable()

        # Label
        arcade.load_font("assets/fonts/IrishGrover-Regular.ttf")

        self.label = gui.UILabel(
            text="Create player username: ",
            text_color=colr.THEME_PINK,
            font_size=self.window.height * 0.05,
            font_name="Irish Grover"
        )

        # Input field (wider + cleaner default text)
        self.input_field = gui.UIInputText(
            color=colr.THEME_LIGHT_BLUE,
            font_size=self.window.height * 0.04,
            width=self.window.width * 0.3,
            height=self.window.height * 0.08,
            text=''
        )

        button_width = self.window.width / 5
        button_height = self.window.height / 12

        # Back button
        self.back_button = button.Button(
            self.window.width * 0.35,
            self.window.height * 0.3,
            button_width,
            button_height,
            "Back",
            colr.THEME_TEAL,
            colr.THEME_DARK_BLUE
        )

        # Continue button
        self.continue_button = button.Button(
            self.window.width * 0.65,
            self.window.height * 0.3,
            button_width,
            button_height,
            "Continue",
            colr.THEME_YELLOW,
            colr.THEME_DARK_BLUE
        )

        # Main vertical layout with spacing
        self.v_box = gui.UIBoxLayout(space_between=20)

        self.v_box.add(self.label)
        self.v_box.add(self.input_field)

        # Anchor layout (center everything)
        anchor = gui.UIAnchorLayout()
        anchor.add(
            self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.manager.add(anchor)

    def on_show_view(self):
        self.background_color = colr.THEME_DARK_BLUE

    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.back_button.draw()
        self.continue_button.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.continue_button.button_pressed(x, y):
            game_view = GameView(self.input_field.text)
            game_view.setup()
            self.window.show_view(game_view)
        if self.back_button.button_pressed(x, y):
            from views.title_view import TitleView
            title_view = TitleView()
            self.window.show_view(title_view)
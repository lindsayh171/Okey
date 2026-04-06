import arcade
from arcade import gui
import assets.colors as colr
from ui_components import button

class NameView(arcade.View):
    """
    View for users to enter their username.
    Passes username to the game once the user continues.
    A username is not required.
    """
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()

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
            [self.window.width * 0.35,
            self.window.height * 0.3],
            [button_width,
            button_height],
            "Back",
            [colr.THEME_TEAL,
            colr.THEME_DARK_BLUE]
        )

        # Continue button
        self.continue_button = button.Button(
            [self.window.width * 0.65,
            self.window.height * 0.3],
            [button_width,
            button_height],
            "Continue",
            [colr.THEME_YELLOW,
            colr.THEME_DARK_BLUE]
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
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.back_button.draw()
        self.continue_button.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.continue_button.button_pressed(x, y):
            # Only continue if a name has been entered
            username = self.input_field.text
            if username:
                self.window.show_game(self.input_field.text)
        if self.back_button.button_pressed(x, y):
            self.window.show_title()

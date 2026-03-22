import arcade

import ui_components.button as button
import assets.colors as colr
from assets.utils import Views


class RulesView(arcade.View):
    def __init__(self, origin):
        super().__init__()

        self.origin = origin
        self.title_text = None
        self.exit_button = None

        # grid to hold rules
        self.rule_sections = []
        self.section_texts = []

        self.objective_text = None
        self.rule_texts = [
            "Taking a Turn:\n\n"
            "Draw from draw pile or previous player's discard (if open)\n"
            "Add tile to your stand, discard it, or play it\n"
            "Every turn ends by discarding",

            "Opening Your Hand:\n\n"
            "Minimum 81 points to open\n"
            "Must exceed previous open value\n"
            "100+ pts → star (-100)",

            "Finishing The Round:\n\n"
            "All tiles in hand must form valid groups",

            "Winning:\n\n"
            "Lowest total score after 6 rounds"
        ]


    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = colr.THEME_DARK_BLUE

        title_x = self.window.width / 2
        title_y = 17 * self.window.height / 20

        button_width = self.window.width / 5
        button_height = self.window.height / 10

        arcade.load_font("assets/fonts/IrishGrover-Regular.ttf")

        # Title text
        self.title_text = arcade.Text(
            "Rules",
            title_x,
            title_y,
            colr.THEME_PINK,
            font_size=self.window.height * 0.1,
            anchor_x="center",
            font_name="Irish Grover"
        )

        self.objective_text = arcade.Text(
            "Objective: Form runs and sets to minimize points.",
            title_x,
            self.window.height * 0.8,
            colr.THEME_YELLOW,
            font_size=self.window.height * 0.03,
            anchor_x="center",
            font_name="Irish Grover"
        )

        # create sections for other rules
        section_width = self.window.width * 0.4
        section_height = self.window.height * 0.22
        left_x = self.window.width / 4
        right_x = self.window.width * 0.75
        top_y = self.window.height * 0.55
        bottom_y = self.window.height * 0.25
        sections = [
            (left_x, top_y),
            (right_x, top_y),
            (left_x, bottom_y),
            (right_x, bottom_y)
        ]

        # create other text
        for i, sect in enumerate(sections):
            self.rule_sections.append((
                sect[0],  # center x
                sect[1],  # center y
                section_width,
                section_height
            ))

            self.section_texts.append(
                arcade.Text(
                    self.rule_texts[i],
                    sect[0],
                    sect[1],
                    colr.THEME_YELLOW,
                    font_size=self.window.height * 0.02,
                    anchor_x="center",
                    anchor_y="center",
                    align="center",
                    multiline=True,
                    width=section_width
                )
            )

        # Exit button
        self.exit_button = button.Button(
            title_x,
            self.window.height / 10,
            button_width,
            button_height,
            "Exit",
            colr.THEME_YELLOW,
            colr.THEME_DARK_BLUE
        )

        self.window.default_camera.use()

    def on_draw(self):
        self.clear()
        self.title_text.draw()

        # Draw rectangles
        for (x, y, w, h) in self.rule_sections:
            arcade.draw_lrbt_rectangle_filled(
                x - w / 2,
                x + w / 2,
                y - h / 2,
                y + h / 2,
                colr.THEME_TEAL
            )

        self.objective_text.draw()

        for t in self.section_texts:
            t.draw()

        self.exit_button.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.exit_button.button_pressed(x, y):
            match self.origin:
                case Views.TITLE:
                    from views.title_view import TitleView
                    next_view = TitleView()
            self.window.show_view(next_view)
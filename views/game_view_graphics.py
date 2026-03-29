import arcade
import assets.colors as colr
import ui_components.button as ui_button

class GameViewGraphics:
    def __init__(self, window, stand_height):
        self.background_color = colr.THEME_LIGHT_BLUE

        # hand score
        self.score_label = arcade.Text(
            "Hand Score",
            window.height * 0.03 + stand_height * 0.75 * 0.5,
            window.height * 0.03 + stand_height * 0.65,
            colr.THEME_DARK_BLUE,
            font_size=15,
            anchor_x="center",
            anchor_y="center",
        )

        # open button, initially set to grey
        self.open_button = ui_button.Button([window.width * 0.9,
                                             window.height * 0.07],
                                            [window.width / 5,
                                             window.height / 12],
                                            "Open",
                                            [arcade.color.GRAY,
                                             colr.THEME_DARK_BLUE])

        # menu
        self.menu_button = ui_button.Button([window.width * 0.9,
                                             window.height * 0.9],
                                            [window.width / 15,
                                             window.width / 15],
                                            "☰",
                                            [colr.THEME_LIGHT_BLUE,
                                             colr.THEME_DARK_BLUE])

        # end turn button
        self.end_turn_button = ui_button.Button([window.width * 0.9,
                                            window.height * 0.07 + window.height / 11],
                                                [window.width / 5,
                                                window.height / 12],
                                            "End Turn",
                                            [colr.THEME_PINK,
                                            colr.THEME_DARK_BLUE])
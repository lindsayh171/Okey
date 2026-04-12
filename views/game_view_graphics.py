import arcade
import arcade.gui
import assets.colors as colr
import ui_components.button as ui_button
from ui_components.message import Message
import assets.sounds as sounds
from assets.sounds import VOLUME

class GameViewGraphics:
    """
    Basic graphics (score label, buttons) for game view
    """
    def __init__(self, window, stand_height):
        self.window = window
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
                                             window.height * 0.05],
                                            [window.width / 5,
                                             window.height / 12],
                                            "Open",
                                            [colr.GRAY,
                                             colr.THEME_DARK_BLUE])

        # menu
        self.menu_button = ui_button.Button([window.width - ((window.width / 15) / 2),
                                             window.height - ((window.width / 15) / 2)],
                                            [window.width / 15,
                                             window.width / 15],
                                            "☰",
                                            [colr.THEME_LIGHT_BLUE,
                                             colr.THEME_DARK_BLUE])

        # end turn button
        self.end_turn_button = ui_button.Button([window.width * 0.9,
                                            window.height * 0.07 + window.height / 14.5],
                                                [window.width / 5,
                                                window.height / 12],
                                            "End Turn",
                                            [colr.THEME_PINK,
                                            colr.THEME_DARK_BLUE])

        self.open_score = arcade.Text(
            "",
            175,
            self.window.height - 30,
            colr.THEME_TEAL,
            font_size=20,
            anchor_x="center",
            font_name="Irish Grover"
        )

        self.manager = arcade.gui.UIManager()
        # Main vertical layout with spacing
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # Anchor layout (center everything)
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.manager.add(anchor)

        # keep track of what popup is active and hide if new one
        self.active_popup = None

    def show_popup(self, text):
        self.manager.enable()
        # If a popup is already active, remove it
        if self.active_popup:
            self.manager.remove(self.active_popup)
            self.active_popup = None

        # Create and show the new popup
        self.active_popup = Message(self.manager, text)
        self.active_popup.show()

        arcade.play_sound(sounds.error, VOLUME)

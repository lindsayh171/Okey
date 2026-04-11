import arcade

from ui_components import button
import assets.colors as colr
from assets.utils import Views


class ScoreboardView(arcade.View):
    """
    View displaying the game rules.
    Exits back to previous screen
    """
    def __init__(self, origin, game, game_view=None, round_end=False):
        super().__init__()

        self.origin = origin
        self.game = game
        self.game_view = game_view
        self.title_text = None
        self.exit_button = None
        self.round_end = round_end
        self.scoreboard_y = 17 * self.window.height / 20

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = colr.THEME_DARK_BLUE

        scoreboard_x = self.window.width / 2
        button_width = self.window.width / 5
        button_height = self.window.height / 10

        arcade.load_font("assets/fonts/IrishGrover-Regular.ttf")

        # Exit/Continue button
        if self.round_end:
            self.exit_button = button.Button(
                [scoreboard_x,
                 self.window.height / 10],
                [button_width * 1.4,
                 button_height],
                "Continue",
                [colr.THEME_TEAL,
                 colr.THEME_DARK_BLUE]
            )

            # Title text
            self.title_text = arcade.Text(
                f"Round {self.game_view.game.curr_round - 1} Over.",
                scoreboard_x,
                self.scoreboard_y,
                colr.THEME_PINK,
                font_size=self.window.height * 0.1,
                anchor_x="center",
                font_name="Irish Grover"
            )
        else:
            self.exit_button = button.Button(
                [scoreboard_x,
                self.window.height / 10],
                [button_width,
                button_height],
                "Exit",
                [colr.THEME_TEAL,
                colr.THEME_DARK_BLUE]
            )

            # Title text
            self.title_text = arcade.Text(
                "Scoreboard",
                scoreboard_x,
                self.scoreboard_y,
                colr.THEME_PINK,
                font_size=self.window.height * 0.1,
                anchor_x="center",
                font_name="Irish Grover"
            )

        self.window.default_camera.use()

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        self.exit_button.draw()

        # Displaying scores of each round
        total_rounds = 6

        # Margins of scoreboard
        top_margin = self.scoreboard_y - 150
        row_height = 80
        column_width = 80
        total_score_gap = 100
        border_thickness = 4
        name_width = 250
        star_size = self.window.height * 0.025

        grid_width = name_width + (total_rounds * column_width) + total_score_gap

        board_start_x = self.window.width / 2 - grid_width / 2

        # Draw each player name
        for i, player in enumerate(self.game.players):
            player_y = top_margin - i * row_height

            arcade.draw_text(
                player.name,
                board_start_x,
                player_y,
                colr.THEME_LIGHT_BLUE,
                font_size=30,
                anchor_x="left",
            )

            # draw stars under names
            for index in range(player.stars):
                star = arcade.Text(
                    "★",
                    board_start_x + star_size * index,
                    player_y - 4 * star_size / 3,
                    colr.THEME_YELLOW,
                    font_size=star_size
                )
                star.draw()

            # Display score for each player's turn
            for round_index in range(total_rounds):
                score_x = board_start_x + name_width + (round_index * column_width)
                arcade.draw_lbwh_rectangle_filled(
                    score_x - column_width / 2,
                    player_y - row_height / 2,
                    column_width,
                    row_height,
                    colr.THEME_LIGHT_BLUE,
                )
                arcade.draw_lbwh_rectangle_outline(
                    score_x - column_width / 2,
                    player_y - row_height / 2,
                    column_width,
                    row_height,
                    colr.THEME_YELLOW,
                    border_thickness
                )

                # If player has a score for that turn, display it
                if round_index < len(player.round_scores):
                    arcade.draw_text(
                        str(player.round_scores[round_index]),
                        score_x,
                        player_y,
                        colr.WHITE,
                        font_size=30,
                        anchor_x="center",
                        anchor_y="center",
                    )

            # Draw total scores
            total_score_x = (board_start_x + name_width +
                             (total_rounds * column_width) + total_score_gap)
            arcade.draw_text(
                f"Total: {player.total_score - 100 * player.stars}",
                total_score_x,
                player_y,
                colr.THEME_YELLOW,
                font_size=30,
                anchor_x="center",
                anchor_y="center",
            )

    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.exit_button.button_pressed(x, y):
            if self.round_end:
                self.game_view.setup()
                self.window.show_view(self.game_view)
            else:
                match self.origin:
                    case Views.TITLE:
                        self.window.show_title()
                    case Views.MENU:
                        self.window.show_menu(self.game_view)
                    case Views.END:
                        self.window.show_end(game=self.game)
                    case _:
                        self.window.show_menu(self.game_view)

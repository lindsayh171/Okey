import arcade
from ui_components import button
import assets.colors as colr
from assets.utils import Views

class EndView(arcade.View):
    """
    End of game with scoreboard, quit and new game options
    """
    def __init__(self, game, user_quit = False):
        super().__init__()

        self.title_text = None
        self.new_button = None
        self.scoreboard_button = None
        self.quit_button = None

        self.game = game

        # check if user quit before ending game
        self.quit = user_quit

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = colr.THEME_DARK_BLUE

        title_x = self.window.width / 2
        title_y = 2* self.window.height / 3

        button_width = (self.window.width / 5) * 1.45
        button_height = self.window.height / 10

        self.title_text = arcade.Text(
            "Thank you for playing.",
            title_x,
            title_y,
            colr.THEME_PINK,
            font_size=self.window.height * 0.1,
            anchor_x="center",
            font_name="Irish Grover"
        )
        if not self.quit:
            place = self.get_place()

            match place:
                case 0:
                    self.title_text = arcade.Text(
                        "1st Place!!\nCongratulations.",
                        title_x,
                        title_y,
                        colr.THEME_PINK,
                        font_size=self.window.height * 0.1,
                        anchor_x="center",
                        anchor_y="center",
                        multiline=True,
                        align="center",
                        width=self.window.width * 0.8,
                        font_name="Irish Grover"
                    )
                case 1:
                    self.title_text = arcade.Text(
                        "2nd Place!\nThank you for playing.",
                        title_x,
                        title_y,
                        colr.THEME_PINK,
                        font_size=self.window.height * 0.1,
                        anchor_x="center",
                        anchor_y="center",
                        multiline=True,
                        align="center",
                        width=self.window.width,
                        font_name="Irish Grover"
                    )
                case 2:
                    self.title_text = arcade.Text(
                        "3rd Place.\nThank you for playing.",
                        title_x,
                        title_y,
                        colr.THEME_PINK,
                        font_size=self.window.height * 0.1,
                        anchor_x="center",
                        anchor_y="center",
                        multiline=True,
                        align="center",
                        width=self.window.width,
                        font_name="Irish Grover"
                    )
                case 3:
                    self.title_text = arcade.Text(
                        "Last Place :(\nThank you for playing.",
                        title_x,
                        title_y,
                        colr.THEME_PINK,
                        font_size=self.window.height * 0.1,
                        anchor_x="center",
                        anchor_y="center",
                        multiline=True,
                        align="center",
                        width=self.window.width,
                        font_name="Irish Grover"
                    )
                case _:
                    self.title_text = arcade.Text(
                        "Thank you for playing.",
                        title_x,
                        title_y,
                        colr.THEME_PINK,
                        font_size=self.window.height * 0.1,
                        anchor_x="center",
                        font_name="Irish Grover"
                    )

        # quit button
        self.quit_button = button.Button([title_x - button_width * 0.8,
                                         title_y - button_height * 3],
                                         [button_width,
                                         button_height],
                                         "Quit",
                                         [colr.THEME_YELLOW,
                                         colr.THEME_DARK_BLUE])

        # new game button
        self.new_button = button.Button([title_x + button_width * 0.8,
                                          title_y - button_height * 3],
                                          [button_width,
                                          button_height],
                                          "New Game",
                                          [colr.THEME_TEAL,
                                          colr.THEME_DARK_BLUE])

        # scoreboard button
        self.scoreboard_button = button.Button([title_x,
                                         title_y - button_height * 4.6],
                                        [button_width,
                                         button_height],
                                        "Scoreboard",
                                        [colr.THEME_TEAL,
                                         colr.THEME_DARK_BLUE])

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.title_text.draw()
        self.new_button.draw()
        self.quit_button.draw()
        if not self.quit:
            self.scoreboard_button.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        if self.new_button.button_pressed(x,y):
            self.window.show_title()
        if self.scoreboard_button.button_pressed(x, y):
            self.window.show_scoreboard(Views.END, self.game)
        if self.quit_button.button_pressed(x, y):
            arcade.close_window()

    def get_place(self):
        player_order = []

        # loop through each player and add based on total score
        for player in self.game.players:
            curr_index = 0
            for ordered_player in player_order:
                if player.total_score >= ordered_player.total_score:
                    curr_index += 1

            player_order.insert(curr_index, player)

        return player_order.index(self.game.players[0])

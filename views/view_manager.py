"""Application window: central place for cross-view navigation (avoids circular imports)."""

import arcade

from assets.utils import Views
from views.game_view import GameView
from views.menu_view import MenuView
from views.name_view import NameView
from views.rules_view import RulesView
from views.title_view import TitleView


class ViewManager(arcade.Window):
    """Arcade window that knows how to switch between all views."""

    def show_title(self):
        self.show_view(TitleView())

    def show_name_entry(self):
        self.show_view(NameView())

    def show_game(self, player_name: str):
        view = GameView(player_name)
        view.setup()
        self.show_view(view)

    def show_rules(self, origin: Views, game_view=None):
        self.show_view(RulesView(origin, game_view))

    def show_menu(self, game_view):
        self.show_view(MenuView(game_view))

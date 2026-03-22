import arcade
from views.title_view import TitleView
from views.rules_view import RulesView

def main():
    window = arcade.Window(1000,
            800,
            "Test Game",
            resizable=True)
    start_view = RulesView("title")
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

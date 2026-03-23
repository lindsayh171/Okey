import arcade
from views.title_view import TitleView

def main():
    window = arcade.Window(1000,
            800,
            "Test Game",
            resizable=False)
    window.game_view = None
    start_view = TitleView()
    window.title_view = start_view
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

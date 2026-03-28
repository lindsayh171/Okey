import arcade
from views.title_view import TitleView

def main():
    window = arcade.Window(1200,
            800,
            "Test Game",
            resizable=False)
    start_view = TitleView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

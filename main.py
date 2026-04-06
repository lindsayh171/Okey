import arcade
from views.view_manager import ViewManager


def main():
    """Runs the game"""
    # Load font once
    arcade.load_font("assets/fonts/Itim-Regular.ttf")
    window = ViewManager(1200, 800, "Okey", resizable=False)
    window.show_title()
    arcade.run()

if __name__ == "__main__":
    main()

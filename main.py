import arcade
from tile import Tile, TILE_WIDTH, TILE_HEIGHT

# Game window class
class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(
            800,
            600,
            "Test Game",
            resizable=True
        )
        self.background_color = arcade.color.FOREST_GREEN

        # List of tiles no matter where they are in game
        self.tile_list = arcade.SpriteList()

    # Set up game
    def setup(self):

        # TODO: maybe separate this out into another file
        x = 0
        y = 300
        for i in range(1, 14):
            # red tile
            tile = Tile(x, y, arcade.color.RED, i)
            self.tile_list.append(tile)
            x+=TILE_WIDTH + 2

            # orange tile
            tile = Tile(x, y, arcade.color.ORANGE, i)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2

            # blue tile
            tile = Tile(x, y, arcade.color.BLUE, i)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2

            # black tile
            tile = Tile(x, y, arcade.color.BLACK, i)
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2

        for i in range(1, 3):
            tile = Tile(x, y, arcade.color.GREEN, "★")
            self.tile_list.append(tile)
            x += TILE_WIDTH + 2



    # Screen render that clears the board
    def on_draw(self):
        self.clear()

        self.tile_list.draw()

        for tile in self.tile_list:
            # Rectangle
            arcade.draw_lbwh_rectangle_filled(
                tile.center_x - TILE_WIDTH / 2,
                tile.center_y - TILE_HEIGHT / 2,
                TILE_WIDTH,
                TILE_HEIGHT,
                (222, 212, 193)
            )

            # Value
            arcade.draw_text(
                str(tile.value),
                tile.center_x,
                tile.center_y + (TILE_HEIGHT / 5),
                tile.value_color,
                40,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            # Symbol
            arcade.draw_text(
                "♥",
                tile.center_x,
                tile.center_y - (TILE_HEIGHT / 3.5),
                tile.value_color,
                15,
                anchor_x="center",
                anchor_y="center"

            def setup_stand(self):
                screen_width = self.width

                # Coordinates of the stand based on the size of the screen
                self.stand_start_x = (screen_width - self.total_stand_width) / 2 + TILE_WIDTH / 2

                # 2 rows in the tile stand
                for row in range(self.rows):
                    stand_y = (TILE_HEIGHT / 2) + row * TILE_HEIGHT
                    # 12 slots on each row
                    for column in range(self.columns):
                        # stand_slot position
                        stand_x = self.stand_start_x + column * TILE_WIDTH

                        # create stand_slot and append to the slot list
                        stand_slot = Stand_Slot(stand_x, stand_y, arcade.color.BEAVER)
                        self.stand_slot_list.append(stand_slot)

    # Com setup
    def setup_coms(self):
        screen_width = self.width
        screen_height = self.height

        # Com coordinates
        com1_x = COM_WIDTH
        com1_y = screen_height / 2
        com2_x = self.width / 2
        com2_y = screen_height - COM_WIDTH
        com3_x = screen_width - COM_WIDTH
        com3_y = screen_height / 2

        # Make each com
        com1 = Com(com1_x, com1_y, arcade.color.RED, "Com 1")
        com2 = Com(com2_x, com2_y, arcade.color.YELLOW, "Com 2")
        com3 = Com(com3_x, com3_y, arcade.color.BLUE, "Com 3")

        # Add each com to the list
        self.com_list.append(com1)
        self.com_list.append(com2)
        self.com_list.append(com3)

    # Discard piles setup
    def setup_discard(self):

        # Placing discards on thirds of the screen size
        third_width = self.width / 3
        third_height = self.height / 3

        # Discard pile coordinates
        left_disc_x = third_width - TILE_WIDTH
        right_disc_x = third_width * 2 + TILE_WIDTH
        top_disc_y = third_height * 2
        bottom_disc_y = third_height

        # Make each discard pile
        com1_disc = Discard(left_disc_x, bottom_disc_y, )
        com2_disc = Discard(right_disc_x, top_disc_y, )
        com3_disc = Discard(left_disc_x, top_disc_y, )
        player_disc = Discard(right_disc_x, bottom_disc_y, )

        # Add discard piles to list
        self.discard_list.append(com1_disc)
        self.discard_list.append(com2_disc)
        self.discard_list.append(com3_disc)
        self.discard_list.append(player_disc)

    # Deck setup
    def setup_deck(self):
        self.deck = Deck(
            self.width / 2,
            self.height / 2,
        )

    # Resize window
    def on_resize(self, width, height):
        super().on_resize(width, height)
        # Run setup again with new screen size
        self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        held_tile = arcade.get_sprites_at_point(x, y), self.tile_list

        self.held_tile = [held_tile]

        self.pull_to_top(self.held_tile[0])

    def on_mouse_release(self, x, y, button, modifiers):

        # If no cards are being held, return
        if len(self.held_tile) == 0:
            return

        # Drop card from held tiles
        self.held_tile = []

    def on_mouse_motion(self, x, y, dx, dy):
        for moving_tile in self.held_tile:
            moving_tile = self.held_tile[0]
            moving_tile.center_x += dx
            moving_tile.center_y += dy

    def pull_to_top(self, selected_tile: arcade.Sprite):
        self.tile_list.remove(selected_tile)
        self.tile_list.append(selected_tile)

def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()


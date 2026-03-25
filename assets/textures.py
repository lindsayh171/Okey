import arcade
import random

TILE_TEXTURE = arcade.make_soft_square_texture(
    80,
    arcade.color.ANTI_FLASH_WHITE,
    outer_alpha=255
)


# All texture assets are free from Kenney.nl
ICON_TEXTURES = [
    "assets/textures/elephant.png",
    "assets/textures/giraffe.png",
    "assets/textures/hippo.png",
    "assets/textures/monkey.png",
    "assets/textures/panda.png",
    "assets/textures/parrot.png",
    "assets/textures/penguin.png",
    "assets/textures/pig.png",
    "assets/textures/rabbit.png",
    "assets/textures/snake.png",
]

def get_random_icon():
    return arcade.load_texture(random.choice(ICON_TEXTURES))
from pathlib import Path
from pygame import image, font
import pygame
from pygame.surface import Surface
from pygame.mixer import Sound

pygame.font.init()

IMG: dict[str, Surface] = {}
SOUND: dict[str, Sound] = {}
FONT = font.Font('font/HomeVideo-BLG6G.ttf', 24)
FONT_BIG = font.Font('font/HomeVideo-BLG6G.ttf', 48)


def get_image(name: str) -> Surface:
    """
    Get an image from the loaded assets

    args:
        name: Name of the image to retrieve
    return:
        Surface: The requested image as a Pygame Surface
    """
    if name in IMG:
        return IMG[name]
    else:
        raise ValueError(f"Image '{name}' not found in assets.")


def get_square_color(color: str, size: int) -> Surface:
    """
    Create a square Surface filled with the specified color.

    args:
        color: The color to fill the square (can be a color name or hex code)
        size: The width and height of the square in pixels
    return:
        Surface: A Pygame Surface object representing the colored square
    """
    try:
        if color == "rainbow":
            return get_image("rainbow")
        surface = Surface((size, size))
        surface.fill(color)
        return surface
    except ValueError:
        raise ValueError(f"Invalid color '{color}' for square.")


def load_image(path: Path) -> None:
    """
    Load all `.png` assets from `path`. Does not work recursively.
    """
    if IMG:          # si ya tiene contenido, no recargar
        return
    for f in path.iterdir():
        if f.suffix == '.png':
            name: str = f.stem
            IMG[name] = image.load(f).convert_alpha()


def load_sound(path: Path) -> None:
    """
    Load all `.mp3` assets from `path`
    """
    if SOUND:
        return
    for f in path.iterdir():
        if f.suffix == '.mp3':
            name: str = f.stem
            SOUND[name] = Sound(f)


def get_sound(name: str) -> Sound:
    """
    Get a sound from the loaded assets

    args:
        name: Name of the sound to retrieve
    """
    if name in SOUND:
        return SOUND[name]
    else:
        raise ValueError(f"Sound '{name}' not found in assets.")

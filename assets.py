from pathlib import Path
from pygame import image
from pygame.surface import Surface


IMG: dict[str, Surface] = {}


def load_image(path: Path) -> None:
    """
    Load all `.png` assets from `path`. Does not work recursively.
    """
    for f in path.iterdir():
        if f.suffix == '.png':
            name: str = str(f).removeprefix('assets/').removesuffix('.png')
            IMG[name] = image.load(f).convert_alpha()

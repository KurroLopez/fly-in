from pygame import Surface, Vector2
import assets
from entities.entities import Hub


class Drone:
    """
    Represents a drone in the simulation.
    """

    img: Surface | None = None
    path: list[Hub]

    def __init__(self, id: int, position: Vector2):
        self.id = id
        self.position = position
        self.img = assets.get_image("drone-small")
        self.path = []

from pygame import Surface, Vector2
import assets
from .hub import Hub
from pathlib import Path


class Drone:
    """
    Represents a drone in the simulation.
    """

    img: Surface | None = None
    __current_hub: Hub | None = None
    __next_hub: Hub | None = None
    __penalty: bool
    __finished: bool

    def __init__(self, id: int, position: Vector2):
        self.id = id
        self.position = position
        assets.load_image(Path("assets"))
        self.img = assets.get_image("drone-small")
        self.__penalty = False
        self.__finished = False

    @property
    def current_hub(self) -> Hub | None:
        """
        Get the current hub for the drone.
        """
        return self.__current_hub

    @current_hub.setter
    def current_hub(self, hub: Hub | None) -> None:
        """
        Set the current hub for the drone.
        """
        self.__current_hub = hub

    @property
    def next_hub(self) -> Hub | None:
        """
        Get the next hub for the drone.
        """
        return self.__next_hub

    @next_hub.setter
    def next_hub(self, hub: Hub | None) -> None:
        """
        Set the next hub for the drone.
        """
        self.__next_hub = hub

    @property
    def is_finished(self) -> bool:
        """
        Check if the drone has finished its path.
        """
        return self.__finished

    def move_to_next_hub(self) -> None:
        """
        Moves the drone to the next hub in its path.
        """
        if not self.__finished:
            if self.__penalty:
                self.__penalty = False
                return

            if self.__next_hub is None:
                return

            if self.__next_hub.is_end:
                self.__finished = True
            print(f"{self.id}:{self.__next_hub.name}")

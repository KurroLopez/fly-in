from typing import Tuple, List
from pygame import Surface, Vector2, Rect
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
    __final_path: List[Tuple[int, str]]
    __in_transit: bool
    __pos: Vector2
    __speed: Vector2
    __rect: Rect

    id: str = ""

    def __init__(self, id: int):
        self.id = f"D{id}"
        
        assets.load_image(Path("assets"))
        self.img = assets.get_image("drone-small")
        self.__penalty = False
        self.__finished = False
        self.__final_path = []
        self.__in_transit = False
        self.__pos = Vector2(0, 0)
        self.__speed = Vector2(0, 0)
        self.__rect = self.img.get_rect(center=self.__pos)

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
        if hub is not None and self.__pos == Vector2(0, 0):
            self.__pos = hub.position
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

    def finished(self, status: bool) -> None:
        """
        Mark the drone as finished or not finished.
        """
        self.__finished = status

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

    def add_final_path(self, turn: int, name: str) -> None:
        """
        Add a hub to the drone's final path.

        Args:
            turn (int): The turn number when the drone reaches the hub.
            hub_name (str): The name of the hub or connection the drone
            is moving to.
        """
        self.__final_path.append((turn, name))

    @property
    def final_path(self) -> List[Tuple[int, str]]:
        """
        Return the list of final path
        """
        return self.__final_path

    @property
    def in_transit(self) -> bool:
        """
        Check if the drone is currently in transit between hubs.
        """
        return self.__in_transit

    @in_transit.setter
    def in_transit(self, status: bool) -> None:
        """
        Set the in-transit status of the drone.
        """
        self.__in_transit = status

    def print(self) -> None:
        """
        Print the drone's final path.
        """
        position: str = ""
        cur_hub: Hub | None = self.__current_hub
        next_hub: Hub | None = self.__next_hub
        if cur_hub is not None and next_hub is not None:
            if self.__in_transit:
                position = f"{cur_hub.name}-{next_hub.name}"
            else:
                position = cur_hub.name
        print(f"{self.id}-{position}", end=' ')

    def draw(self, surface: Surface) -> None:
        """
        Draw the drone on the given surface.

        Args:
            surface (Surface): The surface to draw the drone on.
        """
        if self.img is not None:
            surface.blit(self.img, self.__rect.move(self.__pos))

    @property
    def old_position(self) -> Vector2:
        """
        Get the previous position of the drone.
        """
        return self.__pos

    @property
    def position(self) -> Vector2:
        """
        Get the current position of the drone.

        Returns:
            Vector2: The current position of the drone.
        """
        current_position: Vector2 = Vector2(0, 0)
        chub: Hub | None = self.__current_hub
        nhub: Hub | None = self.__next_hub
        if chub is not None and nhub is not None:
            pos_origin = chub.position
            pos_destination = nhub.position
            if self.__in_transit:
                direction = pos_destination - pos_origin
                distance = direction.length()
                if distance > 0:
                    direction.normalize_ip()
                    transit_position = pos_origin + direction * \
                        (distance * 0.5)
                    current_position = self.__pos.lerp(
                        transit_position, 0.5)
                else:
                    current_position = pos_origin
            else:
                current_position = chub.position
        return current_position

    def update(self) -> None:
        "Update this object's visual information."
        self.__speed *= 0.75
        dest_pos = self.position
        wishdir = dest_pos - self.__pos
        if wishdir.length() > 32:
            self.__speed += (dest_pos - self.__pos).normalize() * 3
        else:
            self.__speed *= 0.5
        self.__pos += self.__speed

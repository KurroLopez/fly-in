from pygame import Vector2
from matplotlib import colors
from enum import Enum


class ZoneType(str, Enum):
    NORMAL = 'normal'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
    BLOCKED = 'blocked'


class TypeHub(str, Enum):
    START = 'start_hub'
    END = 'end_hub'
    HUB = 'hub'


class HubProperties():
    """
    Properties of a hub
    """
    __posX: int
    __posY: int
    __color: str
    __max_drones: int
    __type: ZoneType

    def __init__(self, x: int,
                 y: int,
                 color: str = 'none',
                 type: ZoneType = ZoneType.NORMAL,
                 max_drones: int = 1) -> None:
        """
        Initialize a hub properties

        args:
        x: Int. X Position in the map
        y: Int. Y Position in the map
        color: str. Name of the color to display this hub. By default Empty
        tpye: Type of hub. By default 'normal'
            valid values:
            normal
            restricted
            priority
            blocked
        max: Max number of drones in this hub. By default 1

        exception:
        ValueError if max value is negative or 0
        """
        self.__posX = x
        self.__posY = y
        self.__color = color
        self.__type = type
        if max_drones < 0:
            raise ValueError("'max_drones' must be a postive value.")
        self.__max_drones = max_drones

    @property
    def max_drones(self) -> int:
        """
        Get the max drones available in this hub
        """
        return self.__max_drones

    @max_drones.setter
    def max_drones(self, max: int) -> None:
        """
        Set the max drones available in this hub

        args:
        max: int. Number of drones

        exception:
        ValueError if max value is negative or 0
        """
        if max < 0:
            raise ValueError("'max' must be a postive value.")
        self.__max_drones = max

    @property
    def posX(self) -> int:
        """
        X Position of the hub
        """
        return self.__posX

    @property
    def posY(self) -> int:
        """
        Y Position of the hub
        """
        return self.__posY

    @property
    def type(self) -> ZoneType:
        """
        Type Zone
        """
        return self.__type

    @property
    def color(self) -> str:
        """
        Return the color to display the hub
        """
        return self.__color

    @color.setter
    def color(self, color: str) -> None:
        """
        Define the color to display the hub

        args:
        color: str. Name of the color.
        """
        self.__color = color

    @property
    def rgb(self) -> tuple[float, float, float]:
        return colors.to_rgb(self.__color)


class Hub():
    """
    Definition of a hub. It could be a general hub or a start/goal hub
    """
    __name: str
    __properties: HubProperties
    __position: Vector2
    __is_start: bool
    __is_end: bool
    __current_capacity: int
    __path_to_end: list['Hub']
    __path_to_hub: list['Hub']

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__position = Vector2(0, 0)
        self.__is_start = False
        self.__is_end = False
        self.__current_capacity = 0
        self.__path_to_end = []
        self.__path_to_hub = []

    @property
    def is_start(self) -> bool:
        """
        Return True if the hub is a start hub
        """
        return self.__is_start

    @is_start.setter
    def is_start(self, is_start: bool) -> None:
        """
        Set the hub as a start hub
        """
        self.__is_start = is_start

    @property
    def is_end(self) -> bool:
        """
        Return True if the hub is an end hub
        """
        return self.__is_end

    @is_end.setter
    def is_end(self, is_end: bool) -> None:
        """
        Set the hub as an end hub
        """
        self.__is_end = is_end

    @property
    def name(self) -> str:
        """
        Return the name of the hub
        """
        return self.__name

    @property
    def properties(self) -> HubProperties:
        """
        Return the properties of the hub
        """
        return self.__properties

    @properties.setter
    def properties(self, properties: HubProperties) -> None:
        """
        Set the properties of the hub
        """
        self.__properties = properties

    @property
    def position(self) -> Vector2:
        """
        Return the position of the hub
        """
        return self.__position

    @position.setter
    def position(self, position: Vector2) -> None:
        """
        Set the position of the hub
        """
        self.__position = position

    @property
    def current_capacity(self) -> int:
        """
        Return the current capacity of the hub
        """
        return self.__current_capacity

    def is_full(self) -> bool:
        """
        Return True if the hub is full
        """
        return self.__current_capacity >= self.__properties.max_drones

    def enter_drone(self) -> bool:
        """
        Increment the current capacity of the hub if it is not full
        """
        if self.is_full():
            return False
        self.__current_capacity += 1
        return True

    def exit_drone(self) -> bool:
        """
        Decrement the current capacity of the hub if it is not empty
        """
        if self.__current_capacity <= 0:
            return False
        self.__current_capacity -= 1
        return True

    def add_path_to_end(self, hub: 'Hub') -> None:
        """
        Add a hub to the path to the end hub
        """
        self.__path_to_end.append(hub)

    def add_path_to_hub(self, hub: 'Hub') -> None:
        """
        Add a hub to the path to another hub
        """
        self.__path_to_hub.append(hub)

    @property
    def path_to_end(self) -> list['Hub']:
        """
        Return the path to the end hub
        """
        return self.__path_to_end

    @property
    def path_to_hub(self) -> list['Hub']:
        """
        Return the path to another hub
        """
        return self.__path_to_hub

    def get_cost(self) -> int:
        """
        Get the movement cost for a given zone type.

        Returns:
            int: The cost value (1 for normal/priority, 2 for restricted,
                0 for blocked).
        """
        if self.__properties.type == ZoneType.NORMAL:
            return 1
        elif self.__properties.type == ZoneType.RESTRICTED:
            return 2
        elif self.__properties.type == ZoneType.PRIORITY:
            return 1
        elif self.__properties.type == ZoneType.BLOCKED:
            return 0
        else:
            return 0

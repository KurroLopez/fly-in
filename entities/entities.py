from enum import Enum

from matplotlib import colors


class ZoneType(str, Enum):
    NORMAL = 'normal'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
    BLOCKED = 'blocked'


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
                 max: int = 1) -> None:
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
        """
        self.__posX = x
        self.__posY = y
        self.__color = color
        self.__type = type
        self.__max_drones = max

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
            raise ValueError("'nb_drones' must be a postive value.")
        self.__max_drones = max

    @property
    def posX(self) -> int:
        """
        X Position of the hub
        """
        return self.__posX

    @property
    def poxY(self) -> int:
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
    def rgb(self) -> tuple[int, int, int]:
        return colors.to_rgb(self.__color)


class ConnectionProperties():
    """
    Properties of a connection
    """
    __max_link_capacity: int

    def __init__(self, max: int = 1) -> None:
        self.__max_link_capacity = max

    @property
    def max_link_capacity(self) -> int:
        """
        Return the max capacity of the link
        """
        return self.__max_link_capacity


class Hub():
    """
    Definition of a hub. It could be a general hub or a start/goal hub
    """
    __name: str
    __properties: HubProperties

    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def properties(self) -> HubProperties:
        return self.__properties

    @properties.setter
    def properties(self, properties: HubProperties) -> None:
        self.__properties = properties


class Connection():
    __origin: Hub
    __destination: Hub
    __properties: ConnectionProperties

    def __init__(self, origin: Hub,
                 destination: Hub,
                 properties: ConnectionProperties) -> None:
        self.__origin = origin
        self.__destination = destination
        self.__properties = properties

    def name_origin(self) -> str:
        return self.__origin.name

    def name_destination(self) -> str:
        return self.__destination.name

    @property
    def properties(self) -> ConnectionProperties:
        return self.__properties

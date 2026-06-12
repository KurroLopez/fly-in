from enum import Enum

from matplotlib import colors


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


class Connection():
    __origin: Hub | None
    __destination: Hub | None
    __properties: ConnectionProperties
    __name: str

    def __init__(self, name: str) -> None:
        """
        Initialize a connection

        args:
        name: str. Name of the connection.
            It should be in the format "origin-destination"
        """
        self.__name = name
        self.__origin = None
        self.__destination = None

    def name_origin(self) -> str:
        """
        Return the name of the origin hub
        """
        if self.__name == "":
            return ""
        return self.__name.split("-")[0].strip()

    def name_destination(self) -> str:
        """
        Return the name of the destination hub
        """
        parts = self.__name.split("-")
        if len(parts) < 2:
            return ""
        return parts[1].strip()

    @property
    def origin(self) -> Hub | None:
        """
        Return the origin hub of the connection
        """
        return self.__origin

    @origin.setter
    def origin(self, origin: Hub | None) -> None:
        """
        Set the origin hub of the connection"""
        self.__origin = origin

    @property
    def destination(self) -> Hub | None:
        """
        Return the destination hub of the connection
        """
        return self.__destination

    @destination.setter
    def destination(self, destination: Hub | None) -> None:
        """
        Set the destination hub of the connection
        """
        self.__destination = destination

    @property
    def properties(self) -> ConnectionProperties:
        """
        Return the properties of the connection
        """
        return self.__properties

    @properties.setter
    def properties(self, properties: ConnectionProperties) -> None:
        """
        Set the properties of the connection
        """
        self.__properties = properties

    @property
    def name(self) -> str:
        """
        Return the name of the connection
        """
        return self.__name

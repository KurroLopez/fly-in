from .hub import Hub


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

    def setup_connection_path(self) -> None:
        """
        Setup the path to the destination hub from the origin hub
        """
        if self.__origin is not None and self.__destination is not None:
            self.__origin.add_path_to_hub(self.__destination)
            self.__destination.add_path_to_end(self.__origin)

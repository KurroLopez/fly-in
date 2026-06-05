from entities import Hub
from entities import Connection


class Map():
    __nb_drones: int
    __start_hub: Hub
    __end_hub: Hub
    __hubs: dict[str, Hub]
    __connections: dict[str, Connection]

    def __init__(self) -> None:
        self.__nb_drones = 0
        self.__start_hub = None
        self.__end_hub = None
        self.__hubs = {}
        self.__connections = {}

    @property
    def nb_drones(self) -> int:
        return self.__nb_drones

    @nb_drones.setter
    def nb_drones(self, nb_drones: int) -> None:
        self.__nb_drones = nb_drones

    @property
    def start_hub(self) -> Hub | None:
        return self.__start_hub

    @start_hub.setter
    def start_hub(self, hub: Hub) -> None:
        self.__start_hub = hub

    @property
    def end_hub(self) -> Hub | None:
        return self.__end_hub

    @end_hub.setter
    def end_hub(self, hub: Hub) -> None:
        self.__end_hub = hub

    @property
    def hubs(self) -> dict[str, Hub]:
        return self.__hubs

    @property
    def connections(self) -> dict[str, Connection]:
        return self.__connections

    def add_hub(self, hub: Hub) -> None:
        self.__hubs[hub.name] = hub

    def add_connection(self, connection: Connection) -> None:
        self.__connections[connection.name] = connection

    def exist_hub(self, name: str) -> bool:
        exists_hub: bool = name in self.__hubs
        exists_start: bool = (self.__start_hub is not None
                              and self.__start_hub.name == name)
        exists_end: bool = (self.__end_hub is not None
                            and self.__end_hub.name == name)
        exists: bool = exists_hub or exists_start or exists_end

        return exists

    def exist_connection(self, name: str) -> bool:
        return name in self.__connections

    def exist_start_hub(self) -> bool:
        return self.__start_hub is not None

    def exist_end_hub(self) -> bool:
        return self.__end_hub is not None

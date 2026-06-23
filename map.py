from entities import Hub, TypeHub
from entities import Connection


class Map():
    __nb_drones: int
    __start_hub: Hub | None
    __end_hub: Hub | None
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

    def exist_hub(self, name: str) -> tuple[bool, TypeHub]:
        exists_hub: bool = name in self.__hubs
        exists_start: bool = False
        exists_end: bool = False
        type_hub: TypeHub = TypeHub.HUB
        if self.__start_hub is not None:
            exists_start = self.__start_hub.name == name
            if exists_start:
                type_hub = TypeHub.START
        if self.__end_hub is not None:
            exists_end = self.__end_hub.name == name
            if exists_end:
                type_hub = TypeHub.END
        exists: bool = exists_hub or exists_start or exists_end

        return exists, type_hub

    def exist_connection(self, name: str) -> bool:
        return name in self.__connections

    def exist_start_hub(self) -> bool:
        return self.__start_hub is not None

    def exist_end_hub(self) -> bool:
        return self.__end_hub is not None

    def search_connection(self, hub1: str, hub2: str) -> Connection | None:
        name: str = f"{hub1}-{hub2}"
        if name in self.__connections:
            return self.__connections[name]
        return None

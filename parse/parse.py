from enum import Enum

from entities import TypeHub
from .validator import Validator
from map import Map
from entities import Hub, Connection


class Configs(str, Enum):
    NB_DRONES = 'nb_drones'
    START_HUB = 'start_hub'
    END_HUB = 'end_hub'
    HUB = 'hub'
    CONNECTION = 'connection'


class Parse():
    """
    Evaluate the information of the configuration file and prepare
    a pre-map with the information.
    Parse the value and store the content.
    If there is any issie, it will be raised in a list of items.
    """
    parse_error: list[str] = []
    configs_valid: list[str] = []

    def __init__(self) -> None:
        self.__map = Map()
        self.configs_valid = [cfg.value for cfg in Configs]
        self.first_line = True

    @property
    def list_errors(self) -> list[str]:
        return self.parse_error

    @property
    def map(self) -> Map:
        return self.__map

    def load_map(self, file: str) -> bool:
        """
        Load the map and parse the content

        Note: The name of each elements must be unique.

        Each map has the following format:
        ** nb_drones: value **
        Number of drones. The value must be a positive value

        ** start_hub: name posX posY [metadata]
        Initial zone. The name of the initial zone, position X Y
            and metadata valid:
            color=name_of_color

        ** end_hub: name posX posY [metadata]
        End zone. The name of the goal zone, position X Y
            and metadata valid:
            color=name_of_color

        Args:
            file: Filepath and name of the map

        Return: Boolean
            True: Parse has been sucessfull
            False: Parse has failed
        """

        try:
            lines: list[str] = []
            with open(file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Map file not found: '{file}'")
        except PermissionError:
            raise PermissionError(f"Map file not accessible: '{file}'")

        for line, raw in enumerate(lines, start=1):
            self.__parse_line(line, raw)
        if self.parse_error:
            return False
        return True

    def __parse_line(self, line_number: int, raw: str) -> None:
        try:
            if raw.strip() == "" or raw.strip().startswith('#'):
                return
            if ':' not in raw:
                raise ValueError("Format not valid")

            spl_line = raw.strip().split(':')
            if len(spl_line) != 2:
                raise ValueError(f"Invalid configuration: '{raw.strip()}'")
            # First part: Name of configuration
            # Second part: configuration
            config_name: str = spl_line[0].lower()
            config_value: str = spl_line[1].lower()

            if config_name not in self.configs_valid:
                raise ValueError(f"Config '{config_name} not valid.")

            if config_name == Configs.NB_DRONES:
                self.__parse_nb_drones(line_number, config_value)
            if config_name == Configs.START_HUB:
                self.__parse_start_hub(line_number, config_value)
            if config_name == Configs.END_HUB:
                self.__parse_end_hub(line_number, config_value)
            if config_name == Configs.HUB:
                self.__parse_hub(line_number, config_value)
            if config_name == Configs.CONNECTION:
                self.__parse_connection(line_number, config_value)
            self.first_line = False
        except ValueError as e:
            self.parse_error.append(f"Error line {line_number}: {e}")

    def __parse_nb_drones(self, line: int, raw: str) -> None:
        if not self.first_line:
            raise ValueError("'nb_drones' parameter must be the first line")
        self.__map.nb_drones = Validator().val_nb_drones(raw)

    def __parse_start_hub(self, line: int, raw: str) -> None:
        if self.__map.exist_start_hub():
            raise ValueError("Start hub is defined previously")
        start_hub: Hub = Validator().val_hub(raw)
        info_hub: tuple[bool, TypeHub] = self.__map.exist_hub(start_hub.name)
        if info_hub[0]:
            raise ValueError(f"The name of start_hub '{start_hub.name}' "
                             "is defined previously")
        self.__map.start_hub = start_hub

    def __parse_end_hub(self, line: int, raw: str) -> None:
        if self.__map.exist_end_hub():
            raise ValueError("End hub is defined previously")
        end_hub: Hub = Validator().val_hub(raw)
        info_hub: tuple[bool, TypeHub] = self.__map.exist_hub(end_hub.name)
        if info_hub[0]:
            raise ValueError(f"The name of end_hub '{end_hub.name}' "
                             "is defined previously")
        self.__map.end_hub = end_hub

    def __parse_hub(self, line_number: int, config_value: str) -> None:
        hub: Hub = Validator().val_hub(config_value)
        info_hub: tuple[bool, TypeHub] = self.__map.exist_hub(hub.name)
        if info_hub[0]:
            raise ValueError(f"Hub '{hub.name}' is defined previously")
        self.__map.add_hub(hub)

    def __parse_connection(self, line_number: int, config_value: str) -> None:
        connection: Connection = Validator().val_connection(config_value)
        if self.__map.exist_connection(connection.name):
            raise ValueError(f"Connection '{connection.name}' "
                             f"is defined previously")
        """ Validate if the origin and destination hubs exist """
        info_origin: tuple[bool, TypeHub]
        info_origin = self.__map.exist_hub(connection.name_origin())
        type_origin: TypeHub = info_origin[1]
        exists_origin: bool = info_origin[0]

        if not exists_origin:
            raise ValueError(f"Origin hub '{connection.name_origin()}' "
                             f"does not exist")

        info_destination: tuple[bool, TypeHub]
        info_destination = self.__map.exist_hub(connection.name_destination())
        type_destination: TypeHub = info_destination[1]
        exists_destination: bool = info_destination[0]
        if not exists_destination:
            raise ValueError(f"Destination hub "
                             f"'{connection.name_destination()}' "
                             f"does not exist")

        origin_hub: Hub | None
        if type_origin == TypeHub.START:
            origin_hub = self.__map.start_hub
        elif type_origin == TypeHub.END:
            origin_hub = self.__map.end_hub
        else:
            origin_hub = self.__map.hubs[connection.name_origin()]

        destination_hub: Hub | None
        if type_destination == TypeHub.START:
            destination_hub = self.__map.start_hub
        elif type_destination == TypeHub.END:
            destination_hub = self.__map.end_hub
        else:
            destination_hub = self.__map.hubs[connection.name_destination()]
        connection.origin = origin_hub
        connection.destination = destination_hub
        connection.setup_connection_path()
        self.__map.add_connection(connection)

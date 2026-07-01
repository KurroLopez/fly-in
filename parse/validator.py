from typing import Any
from entities import Hub, Connection
from entities import HubProperties, ConnectionProperties, ZoneType
from matplotlib import colors
import re


class Validator():

    @staticmethod
    def extract_metadata(raw: str) -> tuple[str, str]:
        """
        Extract metadata from a raw string

        args:
            raw: Raw string containing the value and optional metadata
        return:
            tuple: A tuple containing the value and metadata
        """
        metadata = ""
        if "[" in raw:
            raw, metadata = raw.split("[", 1)
            metadata = metadata.rstrip("]").strip()
        return raw.strip(), metadata

    @staticmethod
    def split_metadata(metadata: str) -> dict[str, str]:
        """
        Split metadata into a dictionary

        args:
            metadata: Raw metadata string
        return:
            dict: A dictionary containing the metadata key-value pairs
        """
        metadata_dict = {}
        for item in metadata.split(' '):
            key_value = item.strip().split('=', 1)
            if len(key_value) == 2:
                key = key_value[0].strip().lower()
                value = key_value[1].strip()
                metadata_dict[key] = value
            else:
                raise ValueError(f"Invalid metadata format: '{item.strip()}'")
        return metadata_dict

    @staticmethod
    def val_nb_drones(raw: str) -> int:
        """
        Validate if the number of drones has a valid number

        args:
            raw: Content of the configuration 'nb_drones'
        return:
            int: Value of number of drones
        """
        nb_drones: int = 0
        raw = raw.strip()
        if raw == "":
            raise ValueError("Value cannot be empty")
        try:
            nb_drones = int(raw)
        except ValueError:
            raise ValueError("'nb_drones' must be a integer. "
                             f"Invalid value '{raw}'")
        if nb_drones <= 0:
            raise ValueError("'nb_drones' must be a postive value. "
                             f"Invalid value '{raw}'")
        return nb_drones

    @staticmethod
    def val_hub(raw: str) -> Hub:
        """
        Validate if the hub configuration is valid

        Args:
            raw: Raw content of the hub configuration
        """
        zone_types = [type.value for type in ZoneType]
        raw = raw.strip()
        if raw == "":
            raise ValueError("Value cannot be empty")

        metadata: str = ""
        raw, metadata = Validator.extract_metadata(raw)

        parts = raw.split()
        if len(parts) < 3:
            raise ValueError(f"Invalid hub definition: '{raw.strip()}'")

        name: str = parts[0]
        if not Validator.__valid_name(name):
            raise ValueError(f"Invalid hub name: '{name}'")
        try:
            pos_x: int = int(parts[1])
            pos_y: int = int(parts[2])
        except ValueError:
            raise ValueError(f"Invalid hub coordinates: '{raw.strip()}'")

        color: str = "whitesmoke"
        md: int = 1
        zone_type: ZoneType = ZoneType.NORMAL
        if metadata:
            metadata_dict = Validator.split_metadata(metadata)
            if len(metadata_dict) > 0:
                for key in metadata_dict.keys():
                    value: Any = metadata_dict[key]
                    match key:
                        case 'color':
                            color = value
                            if color != "rainbow":
                                if color not in colors.cnames:
                                    raise ValueError(f"Invalid color value: "
                                                     f"'{color}'")
                        case 'max_drones':
                            try:
                                md = int(value)
                            except ValueError:
                                raise ValueError("Invalid 'max_drones' value:"
                                                 f"'{value}'")
                            if md <= 0:
                                raise ValueError("'max_drones' must be a "
                                                 "positive integer. "
                                                 f"Invalid value: '{md}'")
                        case 'zone':
                            if value not in zone_types:
                                raise ValueError("Invalid 'zone' "
                                                 f"value: '{value}'")
                            zone_type = value
                        case _:
                            raise ValueError(f"Unknown metadata key: '{key}'")

        hub: Hub = Hub(name)
        hub.properties = HubProperties(pos_x, pos_y, color, zone_type, md)
        return hub

    @staticmethod
    def val_connection(raw: str) -> Connection:
        """
        Validate if the connection configuration is valid

        Args:
            raw: Raw content of the connection configuration

        Returns:
            Connection: Validated connection object
        """
        raw = raw.strip()
        if raw == "":
            raise ValueError("Value cannot be empty")

        metadata: str = ""
        raw, metadata = Validator.extract_metadata(raw)

        parts = raw.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid connection definition: '{raw.strip()}'")

        origin_name: str = parts[0].strip()
        destination_name: str = parts[1].strip()
        if origin_name == "" or destination_name == "":
            raise ValueError(f"Origin or destination cannot be empty: '"
                             f"{raw.strip()}'")

        if origin_name == destination_name:
            raise ValueError(f"Origin and destination cannot be the same: '"
                             f"{raw.strip()}'")

        mlc: int = 1
        if metadata:
            metadata_dict = Validator.split_metadata(metadata)
            for key in metadata_dict.keys():
                value: Any = metadata_dict[key]
                match key:
                    case 'max_link_capacity':
                        try:
                            mlc = int(value)
                        except ValueError:
                            raise ValueError(f"Invalid 'max_link_capacity' "
                                             f"value: '{value}'")
                        if mlc <= 0:
                            raise ValueError(f"'max_link_capacity' must be a "
                                             f"positive integer. "
                                             f"Invalid value: '{mlc}'")
                    case _:
                        raise ValueError(f"Unknown metadata key: '{key}'")

        connection: Connection = Connection(raw)
        connection.properties = ConnectionProperties(mlc)
        return connection

    @staticmethod
    def __valid_name(name: str) -> bool:
        """
        Validate if the name is valid

        Args:
            name: Name to validate
        Returns:
            bool: True if the name is valid, False otherwise
        """
        pattern: str = r"^[a-zA-Z0-9_]+$"
        return bool(re.match(pattern, name))

from entities import Hub, Connection
from entities import HubProperties, ConnectionProperties


class Validator():
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
        if raw == "":
            raise ValueError("Value cannot be empty")
        try:
            nb_drones = int(raw)
        except ValueError:
            raise ValueError("'nb_drones' must be a integer."
                             f"Invalid value '{raw}'")
        if nb_drones <= 0:
            raise ValueError("'nb_drones' must be a postive value."
                             f"Invalid value '{raw}'")
        return nb_drones

    @staticmethod
    def val_hub(raw: str) -> Hub:
        raw = raw.strip()
        if raw == "":
            raise ValueError("Value cannot be empty")

        metadata: str = ""
        if "[" in raw:
            raw, metadata = raw.split("[", 1)
            metadata = metadata.rstrip("]").strip()

        parts = raw.split()
        if len(parts) < 3:
            raise ValueError(f"Invalid hub definition: '{raw.strip()}'")

        name: str = parts[0]
        try:
            pos_x: int = int(parts[1])
            pos_y: int = int(parts[2])
        except ValueError:
            raise ValueError(f"Invalid hub coordinates: '{raw.strip()}'")

        color: str = "none"
        if metadata:
            for item in metadata.split(','):
                key_value = item.strip().split('=', 1)
                if len(key_value) == 2 and key_value[0].strip() == 'color':
                    color = key_value[1].strip()

        hub: Hub = Hub(name)
        hub.properties = HubProperties(pos_x, pos_y, color)
        return hub

    @staticmethod
    def val_connection(raw: str) -> Connection:
        raw = raw.strip()
        if raw == "":
            raise ValueError("Value cannot be empty")

        metadata: str = ""
        if "[" in raw:
            raw, metadata = raw.split("[", 1)
            metadata = metadata.rstrip("]").strip()

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

        max_link_capacity: int = 1
        if metadata:
            for item in metadata.split(','):
                key_value = item.strip().split('=', 1)
                if len(key_value) == 2:
                    if key_value[0].strip() == 'max_link_capacity':
                        try:
                            max_link_capacity = int(key_value[1].strip())
                        except ValueError:
                            value: str = key_value[1].strip()
                            raise ValueError(f"Invalid 'max_link_capacity'"
                                             f" value: '{value}'")
        if max_link_capacity <= 0:
            raise ValueError(f"'max_link_capacity' must be a positive integer."
                             f" Invalid value: '{max_link_capacity}'")

        connection: Connection = Connection(raw)
        connection.properties = ConnectionProperties(max_link_capacity)
        return connection

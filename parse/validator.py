from entities import Hub
from entities import HubProperties


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

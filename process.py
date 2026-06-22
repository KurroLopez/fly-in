from map import Map
from entities import Drone, Hub, ZoneType
from pygame import Vector2
from typing import Dict, List, Tuple


class Process:
    __turn: int
    __map: Map
    __drones: list[Drone]
    __shortest_paths: Dict[str, float]

    def __init__(self, map: Map) -> None:
        """
        Initialize the Process with a given Map.
        """
        self.__map = map
        self.__turn = 0
        self.__drones = []
        initial_position: Vector2
        if self.__map.start_hub is not None:
            initial_position = self.__map.start_hub.position
        else:
            initial_position = Vector2(0, 0)

        for id in range(self.__map.nb_drones):
            drone = Drone(id, initial_position)
            drone.current_hub = self.__map.start_hub
            if self.__map.start_hub is not None:
                self.__map.start_hub.enter_drone()
            self.__drones.append(drone)
        self.__shortest_paths = self.__calculate_costs()

    @property
    def turn(self) -> int:
        """
        Get the current turn number.

        return:
            int: The current turn number.
        """
        return self.__turn

    def reset(self) -> None:
        """
        Reset the process to its initial state.
        """
        self.__turn = 0

    def next(self) -> None:
        """
        Move to the next step in the process.
        """
        if self.__drones is None:
            return

        total_finished: int = sum(drone.is_finished for drone in self.__drones)
        if total_finished == len(self.__drones):
            return

        for drone in self.__drones:
            if not drone.is_finished:
                drone.move_to_next_hub()
        self.__turn += 1

    def __calculate_costs(self) -> Dict[str, float]:
        """
        Calculate the shortest paths from the start hub to all other
        hubs in the map.

        return:
            Dict[str, float]: A dictionary mapping hub names to their
            shortest path costs from the start hub.
        """
        distance: Dict[str, float] = {h.name: float('inf')
                                      for h in self.__map.hubs.values()}
        calc: List[Tuple[float, Hub]] = []
        if self.__map.start_hub is not None:
            distance[self.__map.start_hub.name] = float('inf')
        if self.__map.end_hub is not None:
            distance[self.__map.end_hub.name] = 0.0
            calc.append((0, self.__map.end_hub))

        while calc:
            item = self.pop_min(calc)
            dist, hub = item
            if hub.is_start:
                break
            for neighbor in hub.path_to_end:
                if neighbor.properties.type == ZoneType.BLOCKED:
                    continue
                new_distance = dist + hub.get_cost()
                if neighbor.properties.type == ZoneType.PRIORITY:
                    new_distance -= 0.5
                if new_distance < distance[neighbor.name]:
                    distance[neighbor.name] = new_distance
                    calc.append((new_distance, neighbor))
        return distance

    def pop_min(self, list: List[Tuple[float, Hub]]) -> Tuple[float, Hub]:
        item = min(list)
        list.remove(item)
        return item

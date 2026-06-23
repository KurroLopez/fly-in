from map import Map
from entities import Drone, Hub, ZoneType
from pygame import Vector2
from typing import Dict, List, Tuple
from collections import defaultdict


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
            drone.add_final_path(0, self.__map.start_hub.name
                                 if self.__map.start_hub else "")
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

    def restart_drones(self) -> None:
        """
        Restart all drones to their initial state.
        """
        initial_position: Vector2
        if self.__map.start_hub is not None:
            initial_position = self.__map.start_hub.position
        else:
            initial_position = Vector2(0, 0)

        for drone in self.__drones:
            drone.current_hub = self.__map.start_hub
            drone.next_hub = None
            drone.finished(False)
            drone.position = initial_position

    def __calculate_costs(self) -> Dict[str, float]:
        """
        Calculate the shortest paths from the start hub to all other
        hubs in the map.

        return:
            Dict[str, float]: A dictionary mapping hub names to their
            shortest path costs from the start hub.
        """
        index: int = 0
        distance: Dict[str, float] = {h.name: float('inf')
                                      for h in self.__map.hubs.values()}
        calc: List[Tuple[float, int, Hub]] = []
        if self.__map.start_hub is not None:
            distance[self.__map.start_hub.name] = float('inf')
        if self.__map.end_hub is not None:
            distance[self.__map.end_hub.name] = 0.0
            calc.append((0, index, self.__map.end_hub))

        while calc:
            item = self.pop_min(calc)
            dist, _, hub = item
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
                    index += 1
                    calc.append((new_distance, index, neighbor))
        return distance

    def pop_min(self, list: List[Tuple[float,
                                       int,
                                       Hub]]) -> Tuple[float, int, Hub]:
        item = min(list)
        list.remove(item)
        return item

    def calculate_moves(self) -> None:
        """
        Precalculate the moves for each drone based on the shortest paths
        calculated from the start hub to all other hubs.
        """
        turn: int = 0
        in_transit: Dict[str, Tuple[Hub, int, str]] = {}
    
        while not all(drone.is_finished for drone in self.__drones):
            turn += 1
            from_to: Tuple[str, str]
            from_to_used: Dict[Tuple[str, str], int] = defaultdict(int)
            moves: List[Tuple[Drone, Hub | None, bool, str]] = []
            current_hub: Hub | None
            zone_count: Dict[str, int] = {}
            for drone in self.__drones:
                if drone.is_finished or drone.id in in_transit:
                    continue
                if drone.current_hub is None:
                    continue
                count: int = 0
                ch_name = drone.current_hub.name
                if ch_name in zone_count:
                    count = zone_count[ch_name]
                zone_count[ch_name] = count + 1

            total_zone_count: Dict[str, int] = defaultdict(int, zone_count)
            for drone in self.__drones:
                current_hub = drone.current_hub
                if current_hub is None:
                    continue
                if drone.is_finished:
                    moves.append((drone, current_hub, False, ""))
                    continue
                if drone.id in in_transit:
                    dest_hub, remaining_turns, conn_name = in_transit[drone.id]
                    remaining_turns -= 1
                    con: List[str] = conn_name.split("-")
                    from_to = (con[0], con[1])
                    from_to_used[from_to] += 1

                    if remaining_turns == 0:
                        total_zone_count[dest_hub.name] += 1
                        del in_transit[drone.id]
                        moves.append((drone, dest_hub, False, conn_name))
                    else:
                        in_transit[drone.id] = (dest_hub, remaining_turns,
                                                conn_name)
                        moves.append((drone, None, True, conn_name))
                    continue

                best_distance: float = float("inf")
                best_neighbor: Hub | None = None
                best_conn: Tuple[str, str] = ("", "")

                for neighbor in current_hub.path_to_hub:
                    if neighbor.properties.type == ZoneType.BLOCKED:
                        continue
                    conn = self.__map.search_connection(current_hub.name,
                                                        neighbor.name)
                    if conn is None:
                        continue
                    from_to = (current_hub.name, neighbor.name)
                    max_link_capacity: int = conn.properties.max_link_capacity
                    max_drones: int = neighbor.properties.max_drones
                    if from_to_used[from_to] >= max_link_capacity:
                        continue
                    if not neighbor.is_end:
                        if total_zone_count[neighbor.name] >= max_drones:
                            continue

                    distance: float = self.__shortest_paths[neighbor.name]
                    if distance < best_distance:
                        best_distance = distance
                        best_neighbor = neighbor
                        best_conn = from_to

                if best_neighbor is not None:
                    from_to_used[best_conn] += 1
                    total_zone_count[best_neighbor.name] += 1

                    if current_hub.name != best_neighbor.name:
                        total_zone_count[current_hub.name] -= 1

                    if best_neighbor.properties.type == ZoneType.RESTRICTED:
                        conn_name = f"{best_conn[0]}-{best_conn[1]}"
                        in_transit[drone.id] = (best_neighbor, 1, conn_name)
                        moves.append((drone, best_neighbor, True, conn_name))
                    else:
                        moves.append((drone, best_neighbor, False, ""))
                else:
                    moves.append((drone, current_hub, False, ""))

            for drone, dest, is_transit, conn in moves:
                drone.current_hub = dest

                if is_transit and conn:
                    drone.add_final_path(turn, conn)
                elif dest:
                    drone.add_final_path(turn, dest.name)
                    if not dest.is_end:
                        if not self.is_valid_path(dest):
                            raise ValueError("Invalid path")
                    else:
                        drone.finished(True)

    def is_valid_path(self, hub: Hub) -> bool:
        """Check if there the valid path or not from start to end

        Args:
            hub (Hub): Current hub you want check
                if there valid path from it

        Returns:
            bool: If there valid path return True,
                otherwise return False
        """
        valid = False
        distance = self.__shortest_paths.get(hub.name, float("inf"))

        if distance == float("inf"):
            return False

        for neighbor in hub.path_to_hub:
            if neighbor.properties.type != ZoneType.BLOCKED:
                valid = True
        return valid

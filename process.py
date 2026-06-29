from map import Map
from entities import Drone, Hub, ZoneType, Connection
from typing import Dict, List, Tuple, Generator
from collections import defaultdict
import heapq

# (drone, origin, destination, in_transit)
InfoMove = Tuple[str, Hub | None, Hub | None, bool]


class Process:
    __turn: int
    __map: Map
    __drones: list[Drone]
    __shortest_paths: Dict[str, float]
    __all_moves: Dict[int, List[InfoMove]]
    __drones_index: Dict[str, Drone]

    def __init__(self, map: Map) -> None:
        """
        Initialize the Process with a given Map.
        """
        self.__map = map
        self.__turn = 0
        self.__drones = []
        self.__all_moves = defaultdict(list)
        self.__drones_index = {}

        for id in range(self.__map.nb_drones):
            drone = Drone(id)
            drone.current_hub = self.__map.start_hub
            drone.add_final_path(0, self.__map.start_hub.name
                                 if self.__map.start_hub else "")
            if self.__map.start_hub is not None:
                self.__map.start_hub.enter_drone()
            self.__drones.append(drone)
            self.__drones_index[drone.id] = drone
        self.__shortest_paths = self.__calculate_costs()

    @property
    def turn(self) -> int:
        """
        Get the current turn number.

        return:
            int: The current turn number.
        """
        return self.__turn

    @property
    def total_moves(self) -> int:
        """
        Get the total number of moves calculated for the drones.

        return:
            int: The total number of moves.
        """
        if not self.__all_moves or len(self.__all_moves) == 0:
            return 0
        return len(self.__all_moves)

    def search_dron(self, id: str) -> Drone | None:
        return self.__drones_index.get(id)

    def generator_next(self) -> Generator[List[InfoMove],
                                          None, None]:
        """
        Return the next movement of the drones in this turn
        """
        for turn in range(1, len(self.__all_moves) + 1):
            info_turn: List[InfoMove] = self.__all_moves[turn]
            previous: str = ""
            """ Update dron position """
            for item in info_turn:
                dronid: str = item[0]
                dron: Drone | None = self.search_dron(dronid)
                in_transit: bool = item[3]
                origin: Hub | None = item[1]
                dest: Hub | None = item[2]
                if dron is not None:
                    if in_transit:
                        """
                        Check if previous movement is the same area
                        so, move to the final position
                        """
                        previous = dron.final_path[turn - 1][1]
                        if '-' in previous:
                            """ Has finished the transit movement """
                            org_name = previous.split('-')[0]
                            origin = self.__map.search_hub(org_name)
                            in_transit = False
                    dron.current_hub = origin
                    dron.next_hub = dest
                    dron.in_transit = in_transit
            self.__turn = turn
            yield self.__all_moves[turn]

    def restart_drones(self) -> None:
        """
        Restart all drones to their initial state.
        """
        for drone in self.__drones:
            drone.current_hub = self.__map.start_hub
            drone.next_hub = self.__map.start_hub
            drone.in_transit = False
            drone.finished(False)
        self.__turn = 0

    @property
    def drones(self) -> List[Drone]:
        """
        Get the list of drones in the process.

        return:
            List[Drone]: The list of drones.
        """
        return self.__drones

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
        calc: List[Tuple[float, int, str]] = []
        if self.__map.start_hub is not None:
            distance[self.__map.start_hub.name] = float('inf')
        if self.__map.end_hub is not None:
            distance[self.__map.end_hub.name] = 0.0
            heapq.heappush(calc, (0.0, index, self.__map.end_hub.name))

        while calc:
            dist, _, hub_name = heapq.heappop(calc)
            hub: Hub | None = self.__map.search_hub(hub_name)
            if hub is not None:
                if hub.is_start:
                    break
                for neighbor in hub.path_to_end if hub is not None else []:
                    if neighbor.properties.type == ZoneType.BLOCKED:
                        continue
                    new_distance = dist + hub.get_cost()
                    if neighbor.properties.type == ZoneType.PRIORITY:
                        new_distance -= 0.5
                    if new_distance < distance[neighbor.name]:
                        distance[neighbor.name] = new_distance
                        index += 1
                        heapq.heappush(calc, (new_distance, index,
                                              neighbor.name))
        return distance

    def calculate_moves(self) -> None:
        """
        Precalculate the moves for each drone based on the shortest paths
        calculated from the start hub to all other hubs.
        """
        turn: int = 0
        in_transit: Dict[str, Tuple[Hub, int, str]] = {}
        drone: Drone | None
        conn: Connection | None = None

        while not all(drone.is_finished for drone in self.__drones):
            turn += 1
            from_to: Tuple[str, str]
            from_to_used: Dict[Tuple[str, str], int] = defaultdict(int)
            moves: List[Tuple[str, Hub | None, bool, str]] = []
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
            for drone_id, (dest_hub, remaining, _) in in_transit.items():
                total_zone_count[dest_hub.name] += 1
            for drone in self.__drones:
                current_hub = drone.current_hub
                if current_hub is None:
                    continue
                if drone.is_finished:
                    moves.append((drone.id, current_hub, False, ""))
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
                        moves.append((drone.id, dest_hub, False, conn_name))
                    else:
                        in_transit[drone.id] = (dest_hub, remaining_turns,
                                                conn_name)
                        moves.append((drone.id, None, True, conn_name))
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
                        moves.append((drone.id, best_neighbor, True,
                                      conn_name))
                    else:
                        moves.append((drone.id, best_neighbor, False, ""))
                else:
                    moves.append((drone.id, current_hub, False, ""))

            for drone_id, dest, is_transit, conn_name in moves:
                drone = self.search_dron(drone_id)
                if drone is None:
                    continue

                origin_hub = drone.current_hub
                drone.current_hub = dest

                if is_transit and conn_name:
                    drone.add_final_path(turn, conn_name)
                    con = conn_name.split("-")
                    o = self.__map.search_hub(con[0])
                    d = self.__map.search_hub(con[1])
                    if o is not None and d is not None:
                        self.__all_moves[turn].append((drone_id, o, d, True))

                elif dest is not None:
                    drone.add_final_path(turn, dest.name)
                    if dest.is_end:
                        drone.finished(True)
                    else:
                        if not self.is_valid_path(dest):
                            raise ValueError("Invalid path")
                    if origin_hub is not None and origin_hub != dest:
                        self.__all_moves[turn].append((drone_id, origin_hub,
                                                       dest, False))

        """ Save the all moves of all drones by turn """
        origin: Hub | None = None
        destination: Hub | None = None
        orig_dest: List[str] = []
        orig_name: str = ""
        dest_name: str = ""
        for drone in sorted(self.__drones, key=lambda d: d.id):
            if not drone.final_path:
                continue
            for i in range(1, len(drone.final_path)):
                turn, loc = drone.final_path[i]
                _, prev_loc = drone.final_path[i - 1]
                if loc == prev_loc:
                    continue
                """ Search the loc hub """
                origin = self.__map.search_hub(prev_loc)
                destination = self.__map.search_hub(loc)
                if origin is None:
                    """ Its a connection, so the drone is in transit """
                    orig_dest = prev_loc.split('-')
                    orig_name = orig_dest[0]
                    dest_name = orig_dest[1]
                    conn = self.__map.search_connection(orig_name, dest_name)
                    if conn is not None:
                        origin = self.__map.search_hub(orig_name)
                        destination = self.__map.search_hub(dest_name)
                        if origin is not None and destination is not None:
                            self.__all_moves[turn].append((drone.id, origin,
                                                           destination, True))
                else:
                    if destination is not None:
                        self.__all_moves[turn].append((drone.id, origin,
                                                       destination, False))
                    else:
                        """ Its a connection, so the drone is in transit """
                        orig_dest = loc.split('-')
                        destination = self.__map.search_hub(orig_dest[1])
                        self.__all_moves[turn].append((drone.id, origin,
                                                       destination, True))
                if origin is not None:
                    if origin.is_end:
                        break

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

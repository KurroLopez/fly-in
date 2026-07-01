*This project has been created as part of the 42 curriculum by fralopez*

# Description

The aim of the project is to design and implement an efficient routing and simulation system for a fleet of drones in a dynamic network of interconnected zones.

## Time optimization:
The central purpose is to move all drones from a single starting zone to a single destination zone in the fewest possible simulation turns.

## Adaptive routing algorithm:
Develop an algorithm capable of distributing drones across multiple routes (whether disjoint or overlapping), managing strategic waiting when movement is not possible, and avoiding path conflicts, collisions, or deadlocks.

## Dynamic constraint management:
The system must strictly adhere to movement costs based on zone type (normal, restricted, or priority), avoid blocked zones, and comply with maximum simultaneous occupancy capacities in both zones (max_drones) and connections (max_link_capacity).

## Step-by-step simulation:
Create an engine that evaluates and processes the simulation in discrete turns, validating that the movements comply with the physical and capacity rules at each instant, and generating a formatted text output with the exact movements for each turn.

## Visual representation:
Provide visual feedback on the simulation status through a graphical interface, a color-coded terminal, or both, to improve the user experience and facilitate understanding of the fleet's movement.

# Algorithm & Implementation Strategy

The `Process` class implements a turn-based cooperative pathfinding algorithm with explicit capacity reservation and restricted-zone transit handling.

## 1\. Pre-computation

The algorithm begins with Dijkstra search from the `end_hub`.

- **Distance map**: All zone distances are initialized to infinity, except `end_hub` which is set to 0.
- **Reverse expansion**: The search explores neighbors through the reverse adjacency list (`path_to_end`). Blocked zones are skipped.
- **Terrain cost**: Movement cost is based on zone type: normal and priority zones cost `1`, restricted zones cost `2`. Priority zones receive a heuristic bias by subtracting `0.5` from their cost, encouraging route selection through them.
- **Result**: The computed distance map is stored in `self.__shortest_paths` and used during move selection.
- **Final movements**: All the movements by drones is stored in `self.__all_moves` and read by a Generation function.

## 2\. Turn Order and Drone Evaluation

Drones are processed in a deterministic order each turn.

- **Sorting**: The implementation attempts to sort drones with the heuristic map. Since the pathfinder looks up distances using name's drone current_zone, the order remains stable and reproducible.
- **Effect**: Stable ordering avoids nondeterministic move conflicts when several drones compete for the same connection.
- **Double step**: If an hub is restricted zone, the movement is done in double step, the first one is in transit, the dron is in the connection, and it needs other step to get final hub.

## 3\. Per-turn Move Selection

The algorithm runs a discrete turn loop until every drone reaches the goal.

# Instructions

To run the simulation use the following instruction:

```bash
make run MAP=<path/map.txt>
```

To check the quality of the code, run the following instruction:
```bash
make lint
```

To check the quality as strict mode of the code, run the following instruction:
```bash
make lint-strict
```

# Score
| Difficulty | Map Name | Maximum Score | Score Obtained |
|-|-|-|-|
| easy | 01_linear_path.txt | 6 | 4 |
| easy | 02_simple_fork.txt | 8 | 4 |
| easy | 03_basic_capacity.txt | 6 | 4 |
| medium | 01_dead_end_trap.txt | 12 | 8 |
| medium | 02_circular_loop.txt | 15 | 15 |
| medium | 03_priority_puzzle.txt | 12 | 7 |
| hard | 01_maze_nightmare.txt | 30 | 14 |
| hard | 02_circular_loop.txt | 35 | 16 |
| hard | 03_priority_puzzle.txt | 45 | 26 |
| challenger | 01_the_impossible_dream.txt | 45 | 43 |


# Resources
PyGame documentation | https://www.pygame.org/docs/

Algoritmo de Dijkstra | https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra | https://es.slideshare.net/slideshow/algoritmo-de-dijkstra/59911

HomeVideo font | https://ggbot.itch.io/home-video-font

Music | https://pixabay.com/
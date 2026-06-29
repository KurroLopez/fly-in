from parse import Parse
from sys import argv
from graph import Graph
import format


def main() -> None:
    """
    Main function to run the program.
    It checks for command-line arguments, loads the map, checks for errors,
    and displays the map if no errors are found.

    Usage:
    uv run python3 fly-in.py <file>
    make run MAP=<file>
    """
    len_args = len(argv)
    if len_args == 1:
        print(f"{format.WARNING}Usage:  uv run python3 fly-in.py <file>\n"
              f"{format.TAB}make run MAP=<file>{format.CLEAR}")
        return
    filename: str = argv[1]

    parse: Parse = Parse()
    parse.load_map(filename)
    if parse.list_errors:
        print(f"{format.ERROR}Errors found in {filename}:{format.CLEAR}")
        for error in parse.list_errors:
            print(f"{format.TAB}{format.ERROR}** {error}{format.CLEAR}")
        exit()
    else:
        print(f"{format.BOLD}No errors found in {filename}{format.CLEAR}")
        print(f"{format.BOLD}Displaying map...{format.CLEAR}")
        try:
            graph: Graph = Graph(map=parse.map)
        except ValueError as error:
            print(f"{format.ERROR}Errors found in {filename}:{format.CLEAR}")
            print(f"{format.TAB}{format.ERROR}** {error}{format.CLEAR}")
            exit()
        graph.run()
        print(f"{format.BOLD}End game{format.CLEAR}")


if __name__ == "__main__":
    main()

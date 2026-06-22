from parse import Parse
from sys import argv
from graph import Graph


"""Text formatting using ANSI escape codes."""
CLEAR: str = '\033[0m'  # Remove all text formatting.
BOLD: str = '\033[1m'  # Bold text formatting.
ERROR: str = '\033[1;91m'  # Red text formatting for errors.
WARNING: str = '\033[93m'  # Yellow text formatting for warnings.
TAB: str = '\t'  # Tab character for indentation.


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
        print(f"{WARNING}Usage:  uv run python3 fly-in.py <file>\n"
              f"{TAB}make run MAP=<file>{CLEAR}")
        return
    filename: str = argv[1]

    parse: Parse = Parse()
    parse.load_map(filename)
    if parse.list_errors:
        print(f"{ERROR}Errors found in {filename}:{CLEAR}")
        for error in parse.list_errors:
            print(f"{TAB}{ERROR}** {error}{CLEAR}")
        exit()
    else:
        print(f"{BOLD}No errors found in {filename}{CLEAR}")
        print(f"{BOLD}Displaying map...{CLEAR}")
        graph: Graph = Graph(map=parse.map)
        graph.run()
        print(f"{BOLD}End game{CLEAR}")


if __name__ == "__main__":
    main()

from parse import Parse
from sys import argv


def main() -> None:
    len_args = len(argv)
    if len_args == 1:
        print("Usage: test.py <file>")
        return
    filename: str = argv[1]

    parse: Parse = Parse()
    parse.load_map(filename)
    if parse.list_errors:
        print(f"Errors found in {filename}:")
        for error in parse.list_errors:
            print(error)
    else:
        print(f"No errors found in {filename}")


if __name__ == "__main__":
    main()

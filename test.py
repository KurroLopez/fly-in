from parse import Parse


def test_parse():
    parser_ok: Parse = Parse()
    assert parser_ok.load_map("maps/test1.txt")
    for error in parser_ok.list_errors:
        print(error)

    parser_ko: Parse = Parse()
    assert not parser_ko.load_map("maps/test2.txt")
    for error in parser_ko.list_errors:
        print(error)


if __name__ == "__main__":
    test_parse()

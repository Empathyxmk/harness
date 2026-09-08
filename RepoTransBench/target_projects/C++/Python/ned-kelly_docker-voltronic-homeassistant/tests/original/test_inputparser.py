from src.inverter_cli.inputparser import InputParser


def test_cmd_option_exists_true():
    argv = ["program", "-f", "file.txt", "-d"]
    argc = len(argv)
    parser = InputParser(argc, argv)
    assert parser.cmdOptionExists("-f")
    assert parser.cmdOptionExists("-d")

def test_cmd_option_exists_false():
    argv = ["program", "-f", "file.txt"]
    argc = len(argv)
    parser = InputParser(argc, argv)
    assert not parser.cmdOptionExists("-z")

def test_get_cmd_option_with_value():
    argv = ["program", "-f", "file.txt", "-x", "val"]
    argc = len(argv)
    parser = InputParser(argc, argv)
    assert parser.getCmdOption("-f") == "file.txt"
    assert parser.getCmdOption("-x") == "val"

def test_get_cmd_option_missing_or_no_value():
    argv = ["program", "-f"]
    argc = len(argv)
    parser = InputParser(argc, argv)
    assert parser.getCmdOption("-f") == ""
    assert parser.getCmdOption("-notfound") == ""
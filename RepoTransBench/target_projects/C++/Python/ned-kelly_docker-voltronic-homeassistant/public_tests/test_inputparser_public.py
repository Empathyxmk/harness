from src.inverter_cli.inputparser import InputParser

def test_cmd_option_exists_different_input():
    argv = ["foo", "--alpha", "data.log", "--beta"]
    argc = len(argv)
    parser = InputParser(argc, argv)
    assert parser.cmdOptionExists("--alpha")
    assert parser.cmdOptionExists("--beta")

def test_cmd_option_exists_not_found_different_input():
    argv = ["foo", "--alpha", "data.log"]
    argc = len(argv)
    parser = InputParser(argc, argv)
    assert not parser.cmdOptionExists("--nope")
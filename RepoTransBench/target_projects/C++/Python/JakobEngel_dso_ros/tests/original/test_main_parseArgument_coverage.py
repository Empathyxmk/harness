import pytest

def parseArgument(argc, argv):
    if argv is None or argc <= 0:
        return -1
    args = []
    if argv:
        for i in range(argc):
            if i >= len(argv) or argv[i] is None:
                break
            args.append(argv[i])
    if not args or (isinstance(args, list) and len(args) == 0):
        return -1
    if "--help" in args or "-h" in args:
        return 0
    if "--version" in args:
        return 0
    if "--config" in args:
        pos = args.index("--config")
        if pos == len(args) - 1:
            return -1
        else:
            return 1
    if len(args) == 1:
        return -1
    for arg in args:
        if arg and (arg.startswith("--") or arg.startswith("-")) and arg not in ("--help", "--version", "--config", "-h"):
            return -1
    return -1


def test_handles_no_arguments():
    argv = []
    argc = 0
    assert parseArgument(argc, argv) == -1

def test_handles_help_argument():
    argv = ["dso", "--help"]
    argc = 2
    assert parseArgument(argc, argv) == 0

def test_handles_version_argument():
    argv = ["dso", "--version"]
    argc = 2
    assert parseArgument(argc, argv) == 0

def test_handles_invalid_argument():
    argv = ["dso", "--unknown"]
    argc = 2
    assert parseArgument(argc, argv) == -1

def test_handles_valid_config_with_extra():
    argv = ["dso", "--config", "path/to/config.yaml", "--run"]
    argc = 4
    assert parseArgument(argc, argv) == 1

def test_handles_valid_config():
    argv = ["dso", "--config", "file.yaml"]
    argc = 3
    assert parseArgument(argc, argv) == 1

def test_handles_missing_config_value():
    argv = ["dso", "--config"]
    argc = 2
    assert parseArgument(argc, argv) == -1

def test_handles_double_dash_empty():
    argv = ["dso", "--", "somearg"]
    argc = 3
    assert parseArgument(argc, argv) == -1

def test_handles_many_arguments():
    argv = ["dso", "--config", "cfg.yaml", "extra", "--version"]
    argc = 5
    assert parseArgument(argc, argv) == 1

def test_handles_short_flag():
    argv = ["dso", "-h"]
    argc = 2
    assert parseArgument(argc, argv) == 0

def test_handles_single_dash_unknown():
    argv = ["dso", "-x"]
    argc = 2
    assert parseArgument(argc, argv) == -1

def test_handles_config_with_special_chars():
    argv = ["dso", "--config", "~/.config&file.yaml"]
    argc = 3
    assert parseArgument(argc, argv) == 1

def test_handles_config_empty_value():
    argv = ["dso", "--config", ""]
    argc = 3
    assert parseArgument(argc, argv) == 1

def test_handles_arguments_with_spaces():
    argv = ["dso", "--config", "my config.yaml"]
    argc = 3
    assert parseArgument(argc, argv) == 1

def test_handles_just_app_name():
    argv = ["dso"]
    argc = 1
    assert parseArgument(argc, argv) == -1
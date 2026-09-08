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

    i = 1
    config_found = False
    while i < len(args):
        if args[i] == "--config":
            if i + 1 >= len(args):
                return -1
            config_found = True
            i += 2
        elif args[i] == "--help":
            if len(args) == 2 and args[1] == "--help":
                return 0
            return -1
        elif args[i].startswith('-'):
            return -1
        else:
            i += 1
    if config_found:
        return 1
    return -1


def test_fuzz_large_argc():
    argv = ["prog", "--unknown1", "foo", "--config", "bar.yaml", "--help", "--config", "x.yaml"]
    argc = len(argv)
    assert parseArgument(argc, argv) == -1

def test_fuzz_null_argv_ptr():
    assert parseArgument(2, None) == -1

def test_fuzz_negative_argc():
    argv = ["prog"]
    argc = -3
    assert parseArgument(argc, argv) == -1

def test_fuzz_empty_string_args():
    argv = [""]
    argc = 1
    assert parseArgument(argc, argv) == -1

def test_fuzz_help_equals_syntax():
    argv = ["prog", "--help=1"]
    argc = 2
    assert parseArgument(argc, argv) == -1

def test_fuzz_config_equals_syntax():
    argv = ["prog", "--config=configfile.yaml"]
    argc = 2
    assert parseArgument(argc, argv) == -1

def test_fuzz_single_dash_config():
    argv = ["prog", "-config", "foo.yaml"]
    argc = 3
    assert parseArgument(argc, argv) == -1
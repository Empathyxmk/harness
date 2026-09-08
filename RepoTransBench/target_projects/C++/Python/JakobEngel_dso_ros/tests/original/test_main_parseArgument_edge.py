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
    return 0

def test_handles_nullptr_argv():
    assert parseArgument(2, None) == -1

def test_handles_negative_argc():
    argv = ["dso"]
    argc = -4
    assert parseArgument(argc, argv) == -1

def test_handles_large_argc_no_args():
    assert parseArgument(100, None) == -1

def test_handles_empty_strings_array():
    argv = []
    argc = 0
    assert parseArgument(argc, argv) == -1
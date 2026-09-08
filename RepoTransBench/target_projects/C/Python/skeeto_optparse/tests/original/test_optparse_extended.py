import pytest
from src.optparse import optparse, optparse_long, optparse_arg, optparse_long as OptparseLong
from src.optparse import OPTPARSE_NONE, OPTPARSE_REQUIRED, OPTPARSE_OPTIONAL

class Options:
    def __init__(self):
        self.argv = []
        self.optind = 0
        self.optarg = None
        self.errmsg = None

def optparse_init(options, argv):
    options.argv = list(argv)
    options.optind = 1 if len(argv) > 0 else 0
    options.optarg = None
    options.errmsg = None

def test_empty_argv():
    argv = []
    options = Options()
    optparse_init(options, argv)
    # Should accept empty, return -1
    raise NotImplementedError("Implement optparse for empty argv.")

def test_long_option_basic():
    argv = ["prog", "--option=val"]
    options = Options()
    longopts = [OptparseLong("option", 'o', OPTPARSE_REQUIRED)]
    optparse_init(options, argv)
    raise NotImplementedError("Implement optparse_long for --option=val.")

def test_long_option_noarg():
    argv = ["prog", "--flag"]
    options = Options()
    longopts = [OptparseLong("flag", 'f', OPTPARSE_NONE)]
    optparse_init(options, argv)
    raise NotImplementedError("Implement optparse_long for --flag with no arg.")

def test_long_option_optional():
    argv = ["prog", "--opt=123"]
    options = Options()
    longopts = [OptparseLong("opt", 'x', OPTPARSE_OPTIONAL)]
    optparse_init(options, argv)
    raise NotImplementedError("Implement optparse_long for optional arg.")

def test_non_option_args():
    argv = ["prog", "hello", "world"]
    options = Options()
    optparse_init(options, argv)
    raise NotImplementedError("Detect non-option args at the end.")

def test_ambiguous_longopt():
    argv = ["prog", "--ba"]
    options = Options()
    longopts = [
        OptparseLong("bar", 'b', OPTPARSE_NONE),
        OptparseLong("baz", 'z', OPTPARSE_NONE)
    ]
    optparse_init(options, argv)
    raise NotImplementedError("Handle ambiguous long options.")

def test_short_option_with_arg_next():
    argv = ["prog", "-c", "nextarg"]
    options = Options()
    optparse_init(options, argv)
    raise NotImplementedError("Short option with next argument is argument value.")

# __main__ runs all tests via pytest
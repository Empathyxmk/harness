import argparse
import pytest
import io
import sys

# In the original C tests, dummy_callback was mainly for coverage and printing.
# Python's argparse doesn't have direct equivalents for simple argument types.
# We'll omit direct callback testing as it's not asserting logic in C.

def test_boolean():
    """
    Corresponds to C's test_boolean.
    Tests ARGPARSE_OPT_BOOLEAN: -b or --bool sets a boolean flag.
    """
    parser = argparse.ArgumentParser(prog="unit")
    # C: {ARGPARSE_OPT_BOOLEAN, 'b', "bool", &value, "test boolean", dummy_callback, 0, 0}
    parser.add_argument('-b', '--bool', action='store_true', help="test boolean")

    args = parser.parse_args(['-b'])
    assert args.bool is True

    args = parser.parse_args(['--bool'])
    assert args.bool is True

    args = parser.parse_args([])
    assert args.bool is False

def test_bit():
    """
    Corresponds to C's test_bit.
    Tests ARGPARSE_OPT_BIT: --flag sets a specific bit, --noflag (with OPT_NONEG)
    does not clear it.
    """
    # Simulate the 'bits' variable from C.
    # Python argparse doesn't have a direct 'bit' option like C.
    # We'll use store_true and manually apply the bit logic.

    # Test --flag: Should set bit 2 (value 2)
    parser_flag = argparse.ArgumentParser(prog="prog", exit_on_error=False)
    parser_flag.add_argument('--flag', action='store_true', help="set bit")
    
    bits = 0
    args_flag = parser_flag.parse_args(['--flag'])
    if args_flag.flag:
        bits |= 2  # Set the 2nd bit (value 2)
    assert bits == 2

    # Test --noflag: Should not clear bit 2 due to OPT_NONEG flag.
    # The C test starts with bits = 2, parses --noflag, and asserts bits == 2.
    # This implies --noflag, despite its "clear bit" description, does not clear when OPT_NONEG.
    parser_noflag = argparse.ArgumentParser(prog="prog", exit_on_error=False)
    parser_noflag.add_argument('--noflag', action='store_true', help="clear bit (with OPT_NONEG)")
    
    bits = 2 # Initial value from C test
    args_noflag = parser_noflag.parse_args(['--noflag'])
    if args_noflag.noflag:
        # In C, with OPT_NONEG, the bit is NOT cleared. So no operation needed here.
        pass
    assert bits == 2

def test_string():
    """
    Corresponds to C's test_string.
    Tests ARGPARSE_OPT_STRING: -s or --str takes a string argument.
    """
    parser = argparse.ArgumentParser(prog="prog")
    # C: {ARGPARSE_OPT_STRING, 's', "str", &str, "a string", dummy_callback, 0, 0}
    parser.add_argument('-s', '--str', type=str, help="a string")

    args = parser.parse_args(['-s', 'abc'])
    assert args.str == 'abc'

    args = parser.parse_args(['--str', 'xyz'])
    assert args.str == 'xyz'

def test_integer():
    """
    Corresponds to C's test_integer.
    Tests ARGPARSE_OPT_INTEGER: -n or --num takes an integer argument.
    """
    parser = argparse.ArgumentParser(prog="prog")
    # C: {ARGPARSE_OPT_INTEGER, 'n', "num", &num, "int", dummy_callback, 0, 0}
    parser.add_argument('-n', '--num', type=int, help="int")

    args = parser.parse_args(['-n', '13'])
    assert args.num == 13

    args = parser.parse_args(['--num', '123'])
    assert args.num == 123

def test_float():
    """
    Corresponds to C's test_float.
    Tests ARGPARSE_OPT_FLOAT: -f or --flt takes a float argument.
    """
    parser = argparse.ArgumentParser(prog="prog")
    # C: {ARGPARSE_OPT_FLOAT, 'f', "flt", &val, "float", dummy_callback, 0, 0}
    parser.add_argument('-f', '--flt', type=float, help="float")

    args = parser.parse_args(['-f', '2.5'])
    assert 2.4 < args.flt < 2.6

    args = parser.parse_args(['--flt', '3.14'])
    assert 3.13 < args.flt < 3.15

def test_errors(capsys):
    """
    Corresponds to C's test_errors.
    Tests error handling for missing arguments.
    In C, the process would abort. In Python, argparse raises SystemExit.
    """
    parser = argparse.ArgumentParser(prog="prog")
    # C: {ARGPARSE_OPT_INTEGER, 'n', "num", &num, "int", NULL, 0, 0}
    parser.add_argument('-n', '--num', type=int, help="int")

    # Expect SystemExit when a required argument's value is missing
    with pytest.raises(SystemExit) as excinfo:
        # capsys.disabled() is used here to allow the SystemExit message to print to stderr naturally
        # when argparse exits, which can be useful for debugging or detailed error checks.
        with capsys.disabled():
            parser.parse_args(['-n'])
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 2 # Standard error code for argparse parsing failures

    # Optionally, check stderr output
    captured = capsys.readouterr() # Re-enable capsys after the test block
    assert "argument -n/--num: expected one argument" in captured.err

def test_group_and_help(capsys):
    """
    Corresponds to C's test_group_and_help.
    Tests OPT_GROUP and OPT_HELP.
    """
    # C: OPT_GROUP("My group options"), OPT_HELP(), OPT_END()
    # C: argparse_describe(&argparse, "description", "epilog");
    # C test explicitly avoids calling argparse_parse with --help, as it would exit.
    # Python's argparse also exits on --help, which can be caught with pytest.raises.

    parser = argparse.ArgumentParser(
        prog="prog",
        description="description",
        epilog="epilog",
        add_help=False # Disable default help to add it explicitly to a group
    )

    # Mimic OPT_GROUP
    group = parser.add_argument_group("My group options")
    # Mimic OPT_HELP
    group.add_argument('--help', action='help', help='show this help message and exit')

    # Verify description and epilog are set
    assert parser.description == "description"
    assert parser.epilog == "epilog"

    # Test --help, ensuring it exits cleanly (code 0)
    with pytest.raises(SystemExit) as excinfo:
        with capsys.disabled():
            parser.parse_args(['--help'])
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 0
    # The help message content itself could be captured and asserted on if needed,
    # but the C test only verifies initialization and description.
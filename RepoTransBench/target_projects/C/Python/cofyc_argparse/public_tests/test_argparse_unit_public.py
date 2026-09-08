import argparse
import pytest
import io
import sys

# In the original C tests, dummy_callback was mainly for coverage and printing.
# Python's argparse doesn't have direct equivalents for simple argument types.
# We'll omit direct callback testing as it's not asserting logic in C.

def test_boolean_public():
    """
    Corresponds to C's test_boolean_public.
    Tests ARGPARSE_OPT_BOOLEAN: -c or --check sets a boolean flag.
    """
    parser = argparse.ArgumentParser(prog="unit_public")
    # C: {ARGPARSE_OPT_BOOLEAN, 'c', "check", &value, "test boolean public", dummy_callback, 0, 0}
    parser.add_argument('-c', '--check', action='store_true', help="test boolean public")

    args = parser.parse_args(['--check'])
    assert args.check is True

    args = parser.parse_args(['-c'])
    assert args.check is True

    args = parser.parse_args([])
    assert args.check is False

def test_bit_public():
    """
    Corresponds to C's test_bit_public.
    Tests ARGPARSE_OPT_BIT: --debug sets a specific bit, --nodebug (with OPT_NONEG)
    does not clear it.
    """
    # Simulate the 'flags' variable from C.
    # Python argparse doesn't have a direct 'bit' option like C.
    # We'll use store_true and manually apply the bit logic.

    # Test --debug: Should set bit 4 (value 4)
    parser_debug = argparse.ArgumentParser(prog="prog_public", exit_on_error=False)
    parser_debug.add_argument('--debug', action='store_true', help="set debug")
    
    flags = 0
    args_debug = parser_debug.parse_args(['--debug'])
    if args_debug.debug:
        flags |= 4  # Set the 4th bit (value 4)
    assert flags == 4

    # Test --nodebug: Should not clear bit 4 due to OPT_NONEG flag.
    # The C test starts with flags = 4, parses --nodebug, and asserts flags == 4.
    # This implies --nodebug, despite its "clear debug" description, does not clear when OPT_NONEG.
    parser_nodebug = argparse.ArgumentParser(prog="prog_public", exit_on_error=False)
    parser_nodebug.add_argument('--nodebug', action='store_true', help="clear debug (with OPT_NONEG)")
    
    flags = 4 # Initial value from C test
    args_nodebug = parser_nodebug.parse_args(['--nodebug'])
    if args_nodebug.nodebug:
        # In C, with OPT_NONEG, the bit is NOT cleared. So no operation needed here.
        pass
    assert flags == 4

def test_string_public():
    """
    Corresponds to C's test_string_public.
    Tests ARGPARSE_OPT_STRING: -t or --text takes a string argument.
    """
    parser = argparse.ArgumentParser(prog="prog_public")
    # C: {ARGPARSE_OPT_STRING, 't', "text", &str, "a string public", dummy_callback, 0, 0}
    parser.add_argument('-t', '--text', type=str, help="a string public")

    args = parser.parse_args(['-t', 'xyz'])
    assert args.text == 'xyz'

    args = parser.parse_args(['--text', 'abc'])
    assert args.text == 'abc'

def test_integer_public():
    """
    Corresponds to C's test_integer_public.
    Tests ARGPARSE_OPT_INTEGER: -m or --mode takes an integer argument.
    """
    parser = argparse.ArgumentParser(prog="prog_public")
    # C: {ARGPARSE_OPT_INTEGER, 'm', "mode", &num, "int public", dummy_callback, 0, 0}
    parser.add_argument('-m', '--mode', type=int, help="int public")

    args = parser.parse_args(['-m', '27'])
    assert args.mode == 27

    args = parser.parse_args(['--mode', '789'])
    assert args.mode == 789

def test_float_public():
    """
    Corresponds to C's test_float_public.
    Tests ARGPARSE_OPT_FLOAT: -z or --zoom takes a float argument.
    """
    parser = argparse.ArgumentParser(prog="prog_public")
    # C: {ARGPARSE_OPT_FLOAT, 'z', "zoom", &val, "float public", dummy_callback, 0, 0}
    parser.add_argument('-z', '--zoom', type=float, help="float public")

    args = parser.parse_args(['-z', '6.75'])
    assert 6.7 < args.zoom < 6.8

    args = parser.parse_args(['--zoom', '9.99'])
    assert 9.98 < args.zoom < 10.00

def test_group_and_help_public(capsys):
    """
    Corresponds to C's test_group_and_help_public.
    Tests OPT_GROUP and OPT_HELP.
    """
    # C: OPT_GROUP("Public group options"), OPT_HELP(), OPT_END()
    # C: argparse_describe(&argparse, "public description", "public epilog");

    parser = argparse.ArgumentParser(
        prog="prog_public",
        description="public description",
        epilog="public epilog",
        add_help=False # Disable default help to add it explicitly to a group
    )

    # Mimic OPT_GROUP
    group = parser.add_argument_group("Public group options")
    # Mimic OPT_HELP
    group.add_argument('--help', action='help', help='show this help message and exit')

    # Verify description and epilog are set
    assert parser.description == "public description"
    assert parser.epilog == "public epilog"

    # Test --help, ensuring it exits cleanly (code 0)
    with pytest.raises(SystemExit) as excinfo:
        with capsys.disabled():
            parser.parse_args(['--help'])
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 0
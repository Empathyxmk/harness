import pytest
import math

# --- Mock implementations as per the tested interface ---

def checkCmdLineFlag(argc, argv, flag):
    """Emulates parsing command line flags like -flag from argv."""
    prefix = f'-{flag}'
    for i in range(argc):
        arg = argv[i]
        if arg.startswith(prefix):
            if arg == prefix or arg.startswith(prefix + "="):
                return True
    return False

def getCmdLineParameterInt(argc, argv, param, default):
    """Emulates parsing -param=VAL from argv as integer."""
    prefix = f'-{param}='
    for i in range(argc):
        arg = argv[i]
        if arg.startswith(prefix):
            try:
                return int(arg[len(prefix):])
            except ValueError:
                pass
    return default

def getCmdLineParameterFloat(argc, argv, param, default):
    """Emulates parsing -param=VAL from argv as float."""
    prefix = f'-{param}='
    for i in range(argc):
        arg = argv[i]
        if arg.startswith(prefix):
            try:
                return float(arg[len(prefix):])
            except ValueError:
                pass
    return default

def test_cmdline_flag_returns_false_on_no_args():
    argv = ["testprog"]
    assert not checkCmdLineFlag(1, argv, "foo")

def test_cmdline_flag_returns_true_on_match():
    argv = ["prog", "-plummer"]
    assert checkCmdLineFlag(2, argv, "plummer")

def test_cmdline_flag_returns_false_on_no_match():
    argv = ["prog", "-abc"]
    assert not checkCmdLineFlag(2, argv, "xyz")

def test_get_cmdline_param_int_returns_default_if_missing():
    argv = ["prog"]
    assert getCmdLineParameterInt(1, argv, "iterations", 42) == 42

def test_get_cmdline_param_int_parses_integer():
    argv = ["prog", "-iterations=77"]
    assert getCmdLineParameterInt(2, argv, "iterations", 42) == 77

def test_get_cmdline_param_int_ignores_others():
    argv = ["prog", "-foo=19"]
    assert getCmdLineParameterInt(2, argv, "iterations", 55) == 55

def test_get_cmdline_param_float_returns_default_if_missing():
    argv = ["prog"]
    assert math.isclose(getCmdLineParameterFloat(1, argv, "timestep", 0.123), 0.123, rel_tol=1e-6)

def test_get_cmdline_param_float_parses_float():
    argv = ["prog", "-timestep=1.5"]
    assert math.isclose(getCmdLineParameterFloat(2, argv, "timestep", 0.111), 1.5, rel_tol=1e-6)

def test_get_cmdline_param_float_ignores_others():
    argv = ["prog", "-foo=14.3"]
    assert math.isclose(getCmdLineParameterFloat(2, argv, "timestep", 0.888), 0.888, rel_tol=1e-6)
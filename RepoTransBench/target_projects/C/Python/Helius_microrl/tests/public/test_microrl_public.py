import pytest
from src.microrl import microrl

# Global variables to capture callback arguments, mimicking C's static variables
executed_argc = 0
executed_argv = None

def test_execute_callback(argc: int, argv_list: list):
    """
    Dummy execute callback to capture arguments.
    Corresponds to C's static test_execute_callback.
    """
    global executed_argc, executed_argv
    executed_argc = argc
    executed_argv = argv_list

def test_print_callback(s: str):
    """
    Dummy print callback (no-op).
    Corresponds to C's static test_print_callback.
    """
    pass

def test_sigint_callback():
    """
    Dummy SIGINT callback (no-op).
    Corresponds to C's static test_sigint_callback.
    """
    pass

def test_microrl_init_invocation():
    """
    Test microrl_init for correct callback assignment.
    Corresponds to C's START_TEST(test_microrl_init_invocation).
    """
    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print_callback)

    assert rl.print_func == test_print_callback

def test_microrl_set_execute():
    """
    Test microrl_set_execute_callback for correct callback assignment.
    Corresponds to C's START_TEST(test_microrl_set_execute).
    """
    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print_callback)
    microrl.microrl_set_execute_callback(rl, test_execute_callback)

    assert rl.execute_callback == test_execute_callback

def test_microrl_set_sigint():
    """
    Test microrl_set_sigint_callback for correct callback assignment.
    Corresponds to C's START_TEST(test_microrl_set_sigint).
    """
    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print_callback)
    microrl.microrl_set_sigint_callback(rl, test_sigint_callback)

    assert rl.sigint_callback == test_sigint_callback

def test_microrl_execute_callback_invocation():
    """
    Test that the execute callback is invoked with correct arguments.
    Corresponds to C's START_TEST(test_microrl_execute_callback_invocation).
    """
    global executed_argc, executed_argv
    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print_callback)
    microrl.microrl_set_execute_callback(rl, test_execute_callback)

    executed_argc = 0
    executed_argv = None

    # Use different test data: "delta" and "echo"
    cmd = ["delta", "echo"]
    # In C, rl.execute is called directly as a function pointer.
    # In Python, it's an attribute that holds the callable.
    rl.execute_callback(2, cmd)

    assert executed_argc == 2
    assert executed_argv == cmd
    assert executed_argv[0] == "delta"
    assert executed_argv[1] == "echo"

def test_microrl_execute_callback_zero_args():
    """
    Test execute callback with zero arguments (boundary case).
    Corresponds to C's START_TEST(test_microrl_execute_callback_zero_args).
    """
    global executed_argc, executed_argv
    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print_callback)
    microrl.microrl_set_execute_callback(rl, test_execute_callback)

    executed_argc = -1
    executed_argv = None

    # Use empty argument vector
    cmd = []
    rl.execute_callback(0, cmd)

    assert executed_argc == 0
    assert executed_argv == cmd
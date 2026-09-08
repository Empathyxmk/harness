import pytest
from src.microrl import microrl

# Global buffer to capture print output, mimicking C's static print_buffer
print_buffer = ""

def test_print(s: str):
    """
    Mock print function to capture output for assertions.
    Corresponds to C's static void test_print(const char *s).
    """
    global print_buffer
    print_buffer = s

def test_init_default():
    """
    Test microrl_init with default parameters.
    Corresponds to C's START_TEST(test_init_default).
    """
    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print)

    assert rl.print_func == test_print
    assert rl.prompt_str == ">"
    assert rl.cmdlen == 0
    # C's assert_int_eq(rl.cmdline[0], '\0') is implied by bytearray init to zeros
    assert rl.cmdline[0] == 0

def test_set_echo():
    """
    Test microrl_set_echo.
    Corresponds to C's START_TEST(test_set_echo).
    The C test does not assert on the state change, just calls the function.
    """
    microrl.microrl_set_echo(0)
    microrl.microrl_set_echo(1)
    # No return, just exercise both branches, as in original C test.

def test_insert_char_alnum():
    """
    Test microrl_insert_char with an alphanumeric character.
    Corresponds to C's START_TEST(test_insert_char_alnum).
    """
    global print_buffer
    print_buffer = "" # Clear buffer for this test

    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print)
    
    # In C, memset(&rl, 0, sizeof(rl)) was used, then rl.print and rl.cmdlen were set.
    # microrl_init already sets print and clears cmdline, so manual reset of cmdlen is enough.
    rl.cmdlen = 0
    
    microrl.microrl_insert_char(rl, ord('X')) # ord('X') to get ASCII value

    assert rl.cmdline[0] == ord('X')
    assert rl.cmdlen == 1
    assert print_buffer == "X"

def test_insert_char_overflow_and_ctrlC():
    """
    Test microrl_insert_char for buffer overflow and Ctrl+C.
    Corresponds to C's START_TEST(test_insert_char_overflow_and_ctrlC).
    """
    global print_buffer
    print_buffer = "" # Clear buffer for this test

    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print)
    rl.cmdlen = microrl._COMMAND_LINE_LEN - 1 # Fill buffer almost to capacity

    # Should not add 'Z' due to overflow
    microrl.microrl_insert_char(rl, ord('Z'))
    assert rl.cmdline[rl.cmdlen] == 0 # Should still be null-terminated at the end of original content

    # Insert control char (Ctrl+C)
    microrl.microrl_insert_char(rl, microrl.KEY_ETX)
    assert print_buffer == "^C\n"
    assert rl.cmdlen == 0 # Cmdline should be cleared after Ctrl+C

def test_split_basic():
    """
    Test microrl_split with basic input.
    Corresponds to C's START_TEST(test_split_basic).
    """
    buf = "cmd one two"
    # argv in C is char *argv[5], which means it's an array of pointers to strings.
    # In Python, we expect a list of strings from microrl_split.
    argc, argv = microrl.microrl_split(buf, ' ')

    assert argc == 3
    assert argv[0] == "cmd"
    assert argv[1] == "one"
    assert argv[2] == "two"

def test_split_edge():
    """
    Test microrl_split with edge cases (multiple spaces, empty string, only spaces, no delimiter).
    Corresponds to C's START_TEST(test_split_edge).
    """
    buf = "  a  b "
    argc, argv = microrl.microrl_split(buf, ' ')
    assert argc == 2
    assert argv[0] == "a"
    assert argv[1] == "b"

    empty_buf = ""
    argc, argv = microrl.microrl_split(empty_buf, ' ')
    assert argc == 0
    assert argv == []

    space_buf = "      "
    argc, argv = microrl.microrl_split(space_buf, ' ')
    assert argc == 0
    assert argv == []

    nospace_buf = "token"
    argc, argv = microrl.microrl_split(nospace_buf, ',')
    assert argc == 1
    assert argv[0] == "token"

def test_set_execute_and_complete():
    """
    Test microrl_set_execute_callback and microrl_set_complete_callback.
    Corresponds to C's START_TEST(test_set_execute_and_complete).
    """
    rl = microrl.Microrl()
    microrl.microrl_init(rl, test_print)

    # Dummy functions mimicking C function pointers
    def dummy_execute(argc, argv_list):
        return argc
    def dummy_complete(argc, argv_list):
        return None # C returns NULL for no completion

    microrl.microrl_set_execute_callback(rl, dummy_execute)
    microrl.microrl_set_complete_callback(rl, dummy_complete)

    assert rl.execute_callback == dummy_execute
    assert rl.complete_callback == dummy_complete
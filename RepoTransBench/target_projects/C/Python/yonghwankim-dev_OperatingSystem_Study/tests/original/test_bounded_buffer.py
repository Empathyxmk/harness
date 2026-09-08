import pytest

BUFFER_SIZE = 5
test_buffer = [0] * BUFFER_SIZE
test_in = 0
test_out = 0

def test_insert_item(item):
    global test_in, test_buffer
    test_buffer[test_in] = item
    test_in = (test_in + 1) % BUFFER_SIZE

def test_remove_item():
    global test_in, test_out, test_buffer
    if test_in == test_out:
        return -1, None
    item = test_buffer[test_out]
    test_out = (test_out + 1) % BUFFER_SIZE
    return 0, item

def setup_function(function):
    global test_in, test_out, test_buffer
    test_in = 0
    test_out = 0
    test_buffer = [0] * BUFFER_SIZE

def test_single_insert_remove_fn():
    global test_in, test_out, test_buffer
    val = 42
    test_insert_item(val)
    assert test_in == 1
    assert test_buffer[0] == 42

    res, outval = test_remove_item()
    assert res == 0
    assert outval == 42
    assert test_out == 1

def test_empty_remove_fn():
    global test_in, test_out
    res, outval = test_remove_item()
    assert res == -1
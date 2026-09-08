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

def test_buffer_wraps_around():
    global test_in, test_out
    test_in = 0
    test_out = 0
    # Insert up to wrap
    for i in range(BUFFER_SIZE * 2):
        test_insert_item(i)
    assert test_in == 0
    # Remove all items
    for i in range(BUFFER_SIZE):
        test_remove_item()
    assert test_out == 0

def test_overflow_protection():
    global test_in, test_out
    test_in = 0
    test_out = 0
    for i in range(BUFFER_SIZE):
        test_insert_item(i)
    test_insert_item(100)
    test_remove_item()  # Remove one
    assert test_out == 1
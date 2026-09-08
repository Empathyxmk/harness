def buffer_init_public():
    global test_buffer, test_in, test_out
    BUFFER_SIZE = 5
    test_buffer = [0] * BUFFER_SIZE
    test_in = 0
    test_out = 0

def buffer_push_public(item):
    global test_buffer, test_in
    BUFFER_SIZE = 5
    test_buffer[test_in] = item
    test_in = (test_in + 1) % BUFFER_SIZE

def buffer_pop_public():
    global test_buffer, test_in, test_out
    BUFFER_SIZE = 5
    if test_in == test_out:
        raise Exception("empty")
    value = test_buffer[test_out]
    test_out = (test_out + 1) % BUFFER_SIZE
    return value

def buffer_is_empty_public():
    global test_in, test_out
    return test_in == test_out

def setup_function(function):
    buffer_init_public()

def test_push_and_pop_public():
    buffer_init_public()
    buffer_push_public(42)
    buffer_push_public(777)
    assert buffer_pop_public() == 42
    buffer_push_public(31)
    assert buffer_pop_public() == 777
    assert buffer_pop_public() == 31
    assert buffer_is_empty_public()

def test_interleaved_push_pop_public():
    buffer_init_public()
    buffer_push_public(1001)
    assert buffer_pop_public() == 1001
    buffer_push_public(2022)
    buffer_push_public(2023)
    assert buffer_pop_public() == 2022
    buffer_push_public(3033)
    assert buffer_pop_public() == 2023
    assert buffer_pop_public() == 3033
    assert buffer_is_empty_public()
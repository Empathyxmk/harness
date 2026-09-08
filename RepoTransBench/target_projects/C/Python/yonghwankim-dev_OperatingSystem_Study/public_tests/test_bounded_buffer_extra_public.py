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

def test_more_pushes_than_pops_public():
    buffer_init_public()
    buffer_push_public(100)
    buffer_push_public(200)
    buffer_push_public(300)
    buffer_push_public(400)
    assert buffer_pop_public() == 100
    assert buffer_pop_public() == 200
    assert buffer_pop_public() == 300
    assert buffer_pop_public() == 400
    assert buffer_is_empty_public()

def test_push_pop_alternate_public():
    buffer_init_public()
    buffer_push_public(11)
    assert buffer_pop_public() == 11
    buffer_push_public(21)
    assert buffer_pop_public() == 21
    buffer_push_public(31)
    buffer_push_public(41)
    assert buffer_pop_public() == 31
    assert buffer_pop_public() == 41
    assert buffer_is_empty_public()
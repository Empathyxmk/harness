import pytest
from src.ringbuffer import RingBuffer

# Note: C public tests use ringbuffer_t, ringbuffer_add, ringbuffer_remove, uint8_t
# My RingBuffer class implements `add` and `remove` methods to match these signatures.
# C's `uint8_t buffer[X]` implies a capacity of `X-1` items.

def test_simple_insertion():
    rb = RingBuffer(capacity=7) # Corresponds to uint8_t buffer[8]; capacity 8-1=7

    assert rb.num_items() == 0

    # Insert values 10, 20, 30, 40
    assert rb.add(10) == 1
    assert rb.add(20) == 1
    assert rb.add(30) == 1
    assert rb.add(40) == 1

    assert rb.num_items() == 4

    # Remove (dequeue) two - should get 10, 20
    ret, val = rb.remove()
    assert ret == 1 and val == 10
    ret, val = rb.remove()
    assert ret == 1 and val == 20

    assert rb.num_items() == 2

    # Insert two more values
    assert rb.add(50) == 1
    assert rb.add(60) == 1
    assert rb.num_items() == 4

def test_full_and_empty():
    rb = RingBuffer(capacity=3) # Corresponds to uint8_t buffer[4]; capacity 4-1=3

    # Fill completely
    assert rb.add(111) == 1
    assert rb.add(222) == 1
    assert rb.add(88) == 1
    assert rb.add(77) == 0 # Full, should not add

    assert rb.num_items() == 3 # Only size-1 can be filled

    # Remove all
    ret, val = rb.remove()
    assert ret == 1 and val == 111
    ret, val = rb.remove()
    assert ret == 1 and val == 222
    ret, val = rb.remove()
    assert ret == 1 and val == 88

    # Now it should be empty
    ret, val = rb.remove()
    assert ret == 0 # Should fail, buffer is empty

    assert rb.num_items() == 0

def test_wraparound():
    rb = RingBuffer(capacity=2) # Corresponds to uint8_t buffer[3]; capacity 3-1=2

    # Add and remove to cause wraparound
    assert rb.add(1) == 1
    assert rb.add(2) == 1
    ret, val = rb.remove()
    assert ret == 1 and val == 1

    assert rb.add(3) == 1
    ret, val = rb.remove()
    assert ret == 1 and val == 2
    assert rb.add(4) == 1

    # Now buffer should hold [3, 4] (conceptually); drain
    assert rb.num_items() == 2
    ret, val = rb.remove()
    assert ret == 1 and val == 3
    ret, val = rb.remove()
    assert ret == 1 and val == 4
    
    ret, val = rb.remove()
    assert ret == 0 # empty

def test_buffer_size_edge():
    rb = RingBuffer(capacity=1) # Corresponds to uint8_t buffer[2]; capacity 2-1=1

    data = [42, 17]

    # Only one item of two size can be in buffer
    assert rb.add(data[0]) == 1
    assert rb.add(data[1]) == 0 # Should fail as capacity is 1

    ret, val = rb.remove()
    assert ret == 1 and val == 42

    assert rb.num_items() == 0
import pytest
from src.ringbuffer import RingBuffer

# Helper for pretty printing test results (pytest handles this implicitly)
# #define TEST_OK(msg)   printf("PASS: %s\n", msg)
# #define TEST_FAIL(msg) do { printf("FAIL: %s\n", msg); assert(0); } while(0)

# C's sizeof(buf) gives total buffer size.
# A common C ring buffer implementation leaves one slot empty to distinguish full/empty.
# So, for `char buf[8];`, effective capacity is 7.
# For `char buf[4];`, effective capacity is 3.

def test_init_empty():
    rb = RingBuffer(capacity=7) # Corresponds to char buf[8]
    assert rb.is_empty()
    # TEST_OK("init + empty")

def test_queue_dequeue_single_char():
    rb = RingBuffer(capacity=7) # Corresponds to char buf[8]
    assert rb.queue(ord('A')) # Queue char 'A'
    assert not rb.is_empty()
    success, c = rb.dequeue()
    assert success
    assert c == ord('A')
    assert rb.is_empty()
    # TEST_OK("queue and dequeue single char")

def test_queue_overfill():
    rb = RingBuffer(capacity=7) # Corresponds to char buf[8]
    for i in range(20):
        rb.queue(i) # Queue integers 0-19
    
    # Buffer has capacity 7 (8-1)
    # The C test checks assert(ring_buffer_is_full(&rb) || ring_buffer_num_items(&rb) == 7);
    # My Python `is_full` will be True if `num_items` is 7.
    assert rb.is_full() 
    assert rb.num_items() == 7

    count = 0
    while True:
        success, out = rb.dequeue()
        if success:
            count += 1
        else:
            break
    
    assert count == 7
    # TEST_OK("overfill ring buffer")

def test_queue_arr_and_dequeue_arr():
    rb = RingBuffer(capacity=7) # Corresponds to char buf[8]
    src = [1, 2, 3, 4, 5]
    
    n_queued = rb.queue_arr(src)
    assert n_queued == 5
    assert rb.num_items() == 5

    n_dequeued, out = rb.dequeue_arr(5)
    assert n_dequeued == 5
    assert out == src
    assert rb.is_empty()
    # TEST_OK("queue_arr and dequeue_arr")

def test_peek():
    rb = RingBuffer(capacity=7) # Corresponds to char buf[8]
    for i in range(4):
        rb.queue(ord('A') + i) # Queue 'A', 'B', 'C', 'D'
    
    success, out = rb.peek(2) # Peek at index 2 (which is 'C')
    assert success
    assert out == ord('C')
    # TEST_OK("peek at index")
    
    # Out of range
    success, out = rb.peek(8)
    assert not success
    assert out is None # Value should not change / should be None
    # TEST_OK("peek out of range")

def test_empty_and_full_conditions():
    rb = RingBuffer(capacity=3) # Corresponds to char buf[4]
    
    # Empty at start
    assert rb.is_empty()
    
    # Fill until full (max 3 items for buffer size 4)
    rb.queue(1)
    rb.queue(2)
    rb.queue(3)
    assert rb.is_full()
    assert rb.num_items() == 3

    # Remove one
    success, out = rb.dequeue()
    assert success and out == 1
    assert not rb.is_full()
    assert rb.num_items() == 2
    # TEST_OK("full/empty conditions")

def test_dequeue_empty():
    rb = RingBuffer(capacity=7) # Corresponds to char buf[8]
    
    # In C, `char c = 0x77;` `assert(!ring_buffer_dequeue(&rb, &c));` then `assert(c == 0x77);`
    # This means the variable `c` should not be modified if dequeue fails.
    # In Python, we return (False, None), so the variable `c` would never be assigned the dequeued value.
    initial_c_value = 0x77
    success, c = rb.dequeue()
    assert not success
    assert c is None # Python's way of indicating no value was returned
    # TEST_OK("dequeue on empty buffer")

def test_dequeue_arr_empty():
    rb = RingBuffer(capacity=7) # Corresponds to char buf[8]
    
    # In C, `char out[4] = {0};` `int ret = ring_buffer_dequeue_arr(&rb, out, 4);` `assert(ret == 0);`
    # `out` array content would remain unchanged.
    n_dequeued, out_list = rb.dequeue_arr(4)
    assert n_dequeued == 0
    assert out_list == []
    # TEST_OK("dequeue_arr on empty buffer")
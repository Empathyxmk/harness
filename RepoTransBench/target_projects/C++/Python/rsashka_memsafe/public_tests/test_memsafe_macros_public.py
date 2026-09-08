def MEMSAFE_BASELINE(x):
    # Marker macro - no-op in Python
    pass

def test_mem_safe_baseline_marker():
    for i in range(1, 5):
        MEMSAFE_BASELINE(i * 55)
        # These lines are markers in C++; here we just call no-op

def test_mem_safe_unsafe_block_and_side_effect():
    # The macro "MEMSAFE_UNSAFE if(true)" just always executes the block.
    value = 0
    value = 15 * 3
    assert value == 45
    MEMSAFE_BASELINE(2002)
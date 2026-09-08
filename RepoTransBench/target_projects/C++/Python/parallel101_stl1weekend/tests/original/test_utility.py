def test_allocation_sim():
    # Simulate new (memory allocation reporting)
    allocated = []
    def custom_new(size):
        allocated.append(size)
        return bytearray(size)
    # normal
    b = custom_new(10)
    assert len(b) == 10
    # aligned
    b2 = custom_new(64)
    assert len(b2) == 64
    # with arg
    b3 = custom_new(16)
    assert len(b3) == 16
    assert sum(allocated) == 90
    # simulate construction
    class M: pass
    m = M()
    assert isinstance(m, M)
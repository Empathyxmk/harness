def test_something_simple_public():
    a = 8
    b = 15
    assert a + b == 23

    s = "redisPublic"
    assert s.startswith("red")
    assert not s.endswith("lock")
from protofuzz import values

def test_integral_value_gen():
    g = values.integral_value_gen()
    # Should be iterable and produce at least some values
    vals = [next(g) for _ in range(8)]
    assert all(isinstance(v, int) for v in vals)

def test_float32_value_gen():
    g = values.float32_value_gen()
    vals = [next(g) for _ in range(8)]
    assert all(isinstance(v, float) for v in vals)

def test_string_value_gen():
    g = values.string_value_gen()
    vals = [next(g) for _ in range(6)]
    assert all(isinstance(v, str) for v in vals)
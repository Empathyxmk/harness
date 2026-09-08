import math

def test_stdlib_basic():
    # Universal tests for math/stdlib paths.
    try:
        a = float("42.5")
        print(f"stod('42.5') = {a}")
        b = float("nan")
        print(f"stod('nan') = {b}")
        c = float("inf")
        print(f"stod('inf') = {c}")
        assert math.isnan(b)  # nan
        assert c > 1e308      # inf
        assert math.isclose(a, 42.5)
    except Exception:
        print("exception!")
        assert False, "Exception during stdlib float conversion"
    try:
        float("notanumber")
        assert False, "Expected ValueError for 'notanumber'"
    except ValueError:
        print("invalid_argument caught!")
        assert True
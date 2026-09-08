"""
Public test: functional, different data (uses new values/length).
Scale-and-add similar to SAXPY, but public data.
"""

def test_tutorial_functional_public():
    length = 9  # Chosen distinct size
    x = [2.0] * length
    y = [5.0] * length
    z = [7.5] * length
    alpha = -0.5
    for i in range(length):
        z[i] += alpha * x[i] + y[i]
    expected = 7.5 + (-0.5) * 2.0 + 5.0  # = 11.5
    for value in z:
        assert value == expected
    print(f"Public functional test - vector scale/add OK for length {length}")
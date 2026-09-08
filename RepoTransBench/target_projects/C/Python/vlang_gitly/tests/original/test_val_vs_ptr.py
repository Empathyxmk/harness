def increment_val(n):
    # Example implementation as per the test's implied needs:
    # increment +2 for each call
    return n + 2

def increment_ptr(n_holder):
    # n_holder: expects a mutable element (e.g., list with one element)
    n_holder[0] += 2

def test_increment_val():
    assert increment_val(3) == 5
    assert increment_val(-2) == 0

def test_increment_ptr():
    n = [10]
    increment_ptr(n)
    assert n[0] == 12
    n = [-4]
    increment_ptr(n)
    assert n[0] == -2
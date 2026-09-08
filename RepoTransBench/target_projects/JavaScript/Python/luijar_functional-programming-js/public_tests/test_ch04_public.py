def map_values(f, arr):
    return [f(x) for x in arr]

def filter_values(f, arr):
    return [x for x in arr if f(x)]

def test_public_map_doubler():
    assert map_values(lambda x: x*2, [1,2,3]) == [2,4,6]

def test_public_filter_big():
    assert filter_values(lambda x: x > 5, [2,3,6,7,8]) == [6,7,8]
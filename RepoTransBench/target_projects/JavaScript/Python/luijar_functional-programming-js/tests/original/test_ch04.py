def map_values(f, arr):
    return [f(x) for x in arr]

def filter_values(f, arr):
    return [x for x in arr if f(x)]

def reduce_values(f, arr, init):
    acc = init
    for x in arr:
        acc = f(acc, x)
    return acc

def test_map_values_square():
    assert map_values(lambda x: x*x, [1,2,3]) == [1,4,9]

def test_filter_values_even():
    assert filter_values(lambda x: x%2 == 0, [1,2,3,4]) == [2,4]

def test_reduce_sum():
    assert reduce_values(lambda acc, x: acc + x, [1,2,3,4], 0) == 10

def test_reduce_product():
    assert reduce_values(lambda acc, x: acc * x, [1,2,3,4], 1) == 24

def test_map_values_empty():
    assert map_values(lambda x: x+1, []) == []

def test_filter_values_none():
    assert filter_values(lambda x: False, [1, 2, 3]) == []

def test_reduce_empty():
    assert reduce_values(lambda acc,x: acc+x, [], 22) == 22
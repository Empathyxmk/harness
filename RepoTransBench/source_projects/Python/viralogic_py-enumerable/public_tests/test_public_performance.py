from py_linq.py_linq import Enumerable

def test_public_enumerable_list_performance():
    e = Enumerable(list(range(200)))
    l = list(e)
    assert l == list(range(200))

def test_public_enumerable_tuple_performance():
    e = Enumerable(tuple(range(120)))
    l = list(e)
    assert l == list(range(120))
import pytest
from redisgraph.query_result import QueryResult

class DummyResultSet:
    def __init__(self):
        self.results = [
            ["a", "b"],
            [1, 2],
            [3, 4]
        ]
        self.header = ['a', 'b']
        self.index = -1

    def __iter__(self):
        return iter(self.results[1:])

    def __next__(self):
        self.index += 1
        if self.index >= len(self.results):
            raise StopIteration
        return self.results[self.index + 1]

def test_query_result_basic_methods():
    res_set = DummyResultSet()
    qr = QueryResult(res_set)
    assert hasattr(qr, "__iter__")
    assert hasattr(qr, "__next__")
    qr.header = [("col", "type")]
    assert qr.keys() == ['col']
    qr._position = 0
    assert next(qr, None) is not None
    assert next(iter(qr)) is not None

def test_query_result_str_repr():
    res_set = DummyResultSet()
    qr = QueryResult(res_set)
    r = str(qr)
    assert isinstance(r, str)
    r2 = repr(qr)
    assert isinstance(r2, str)
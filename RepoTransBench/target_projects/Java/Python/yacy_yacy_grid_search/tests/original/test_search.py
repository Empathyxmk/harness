import pytest
from yacy_grid_search.search import Search

def test_query_normal():
    s = Search()
    assert s.query("hello") == "Search results for: hello"

def test_query_empty():
    s = Search()
    assert s.query("") == "No query provided"
    assert s.query(None) == "No query provided"
    assert s.query("  ") == "No query provided"

def test_query_error():
    s = Search()
    with pytest.raises(ValueError) as ex:
        s.query("error")
    assert str(ex.value) == "Invalid query"

def test_is_service_active():
    s = Search()
    assert s.isServiceActive()
import pytest
from yacy_grid_search.search import Search

def test_query_normal():
    s = Search()
    assert s.query("world") == "Search results for: world"
    assert s.query("123") == "Search results for: 123"
    assert s.query("test_case") == "Search results for: test_case"

def test_query_empty_variants():
    s = Search()
    assert s.query("   ") == "No query provided"  # only spaces
    assert s.query(None) == "No query provided"
    assert s.query("\t") == "No query provided"  # tab only

def test_query_error_different_case():
    s = Search()
    for err in ["ERROR", "Error"]:
        with pytest.raises(ValueError) as ex:
            s.query(err)
        assert str(ex.value) == "Invalid query"

def test_is_service_active_still_true():
    s = Search()
    assert s.isServiceActive()
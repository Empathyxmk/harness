import pytest
from linkedin2username import NameMutator

@pytest.mark.parametrize("input_name,expected", [
    # Public test cases use different names with similar cleaning and structure
    ("Sam Lee", {"first": "sam", "last": "lee", "second": ""}),
    ("Ms. Eva O'Brien", {"first": "eva", "last": "obrien", "second": ""}),
    ("Prof. Łukasz Nowak (PhD)", {"first": "lukasz", "last": "nowak", "second": ""}),
    ("María-José Carreño", {"first": "maria", "last": "carreno", "second": ""}),
    ("Chris (CEO) Smithers", {"first": "chris", "last": "smithers", "second": ""}),
])
def test_clean_and_split_name_public(input_name, expected):
    nm = NameMutator(input_name)
    assert nm.name == expected
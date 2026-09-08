import pytest

def test_truth_public():
    # Slightly different, but checks True value
    assert bool("nonempty"), "Expected a non-empty string to evaluate as True"

def test_split_string_public():
    # Use different string content, split on space
    s = "foo bar baz"
    assert s.split() == ["foo", "bar", "baz"]

def test_sorted_list_public():
    # Use a different list and expected sorted output
    lst = [10, 2, 4, 8]
    assert sorted(lst) == [2, 4, 8, 10]

def test_dict_access_public():
    # Use different keys/values
    d = {"alpha": 1, "beta": 2}
    assert d["beta"] == 2
    assert "alpha" in d
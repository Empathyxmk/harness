import pytest

def test_table_empty():
    table = {}
    assert len(table) == 0

def test_table_simple_add_find():
    table = {}
    table["abc"] = "v"
    assert table["abc"] == "v"

def test_table_simple_multi():
    table = {}
    table["abc"] = "v"
    table["abcd"] = "v"
    table["ac"] = "v2"
    assert table["abc"] == "v"
    assert table["abcd"] == "v"
    assert table["ac"] == "v2"

def test_table_special_key():
    table = {}
    key = b'\xff\xff'
    table[key] = "v3"
    assert table[key] == "v3"

def test_table_randomized():
    import random, string
    table = {}
    for num_entries in [1, 5, 10]:
        table.clear()
        for _ in range(num_entries):
            k = ''.join(random.choices(string.ascii_letters, k=8))
            v = ''.join(random.choices(string.ascii_letters, k=20))
            table[k] = v
        # Search for all inserted
        for k in table:
            assert k in table
            assert isinstance(table[k], str)
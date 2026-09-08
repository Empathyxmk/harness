def test_unorderedmap_basic():
    # Just check import of Python dict as unordered_map equivalent
    d = {}
    d['a'] = 1
    assert d['a'] == 1
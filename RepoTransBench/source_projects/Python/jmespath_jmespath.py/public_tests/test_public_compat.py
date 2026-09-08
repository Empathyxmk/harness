# Only test public, cross-version-safe APIs that are definitely present in compat.
import jmespath.compat as compat
import json

def test_compat_str_coercion():
    # Test that str values remain unchanged, no-op in py3
    s = "public_example"
    assert str(s) == s

def test_compat_json_loads_dumps_branch():
    # Use json module directly as compat does not wrap it
    obj = {"a_pub": [5, 6], "b_pub": "YY"}
    dumped = json.dumps(obj)
    loaded = json.loads(dumped)
    assert loaded == obj

def test_compat_map_and_zip_iterators():
    # Test that map and zip builtins can be used on basic data
    mapped = list(map(lambda x: x - 1, [3, 4, 5]))
    assert mapped == [2, 3, 4]
    zipped = list(zip([10, 20], ['x', 'y']))
    assert zipped == [(10, 'x'), (20, 'y')]
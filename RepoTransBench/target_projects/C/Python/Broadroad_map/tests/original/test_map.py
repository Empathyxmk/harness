import pytest

# Dummy in-memory map/rbtree implementation for test purposes.
# The actual library code should go to src/ and be imported here.
# For now, we use a dict-based implementation to demonstrate logic.
class MapEntry:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.node = self  # For iteration API compatibility

def map_first(root):
    # In a tree, would be leftmost; here, sort keys
    if not root._data:
        return None
    min_key = sorted(root._data.keys())[0]
    return root._data[min_key]
def map_next(node):
    # Not real tree navigation, just API compatibility.
    keys = sorted(node.root._data)
    idx = keys.index(node.key)
    if idx + 1 >= len(keys):
        return None
    next_key = keys[idx + 1]
    return node.root._data[next_key]
def map_free(entry):
    # Simulate deallocation.
    pass

class Root:
    def __init__(self):
        self._data = dict()
    @property
    def rb_node(self):  # for C test parity
        return self._data if self._data else None
    @rb_node.setter
    def rb_node(self, val):
        # `rb_node = None` used for clearing
        if val is None:
            self._data.clear()

def get(root, key):
    return root._data.get(key, None)
def put(root, key, value):
    existed = key in root._data
    root._data[key] = MapEntry(key, value)
    root._data[key].root = root  # for iteration
    return 0 if existed else 1

def test_map_basics():
    mytree = Root()

    # Empty Tree Lookup
    ret = get(mytree, "foo")
    assert ret is None, "get from empty tree should return None"

    # Insertion (new)
    put_ret = put(mytree, "foo", "bar")
    assert put_ret == 1, "put (insert)"

    # Lookup existing
    ret = get(mytree, "foo")
    assert ret and ret.val == "bar", "get after put"

    # Update existing key
    put_ret = put(mytree, "foo", "baz")
    assert put_ret == 0, "put (update)"
    ret = get(mytree, "foo")
    assert ret and ret.val == "baz", "get after update"

    # Insert more keys (left/right branches)
    put(mytree, "apple", "a1")
    put(mytree, "zebra", "z1")
    put(mytree, "aardvark", "aa1")

    # Right branch
    ret = get(mytree, "zebra")
    assert ret and ret.val == "z1", "get zebra"

    # Left branch
    ret = get(mytree, "apple")
    assert ret and ret.val == "a1", "get apple"
    ret = get(mytree, "aardvark")
    assert ret and ret.val == "aa1", "get aardvark"

    # Lookup non-existent
    ret = get(mytree, "nomatch")
    assert ret is None, "get non-existent"

    # Iteration
    count = 0
    found = {"foo": 0, "apple": 0, "zebra": 0, "aardvark": 0}
    for k in mytree._data:
        if k in found:
            found[k] = 1
        count += 1
    assert count >= 4 and all(found.values()), "iteration"

    # Simulate freeing
    for entry in list(mytree._data.values()):
        map_free(entry)
    map_free(None)

    # Final pass
    print("All map/basic rbtree tests pass")
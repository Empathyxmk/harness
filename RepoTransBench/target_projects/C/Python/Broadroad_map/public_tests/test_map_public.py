import pytest

class MapEntry:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.node = self

def map_first(root):
    if not root._data:
        return None
    min_key = sorted(root._data.keys())[0]
    return root._data[min_key]
def map_next(node):
    keys = sorted(node.root._data)
    idx = keys.index(node.key)
    if idx + 1 >= len(keys):
        return None
    next_key = keys[idx + 1]
    return node.root._data[next_key]
def map_free(entry):
    pass

class Root:
    def __init__(self):
        self._data = dict()
    @property
    def rb_node(self):
        return self._data if self._data else None
    @rb_node.setter
    def rb_node(self, val):
        if val is None:
            self._data.clear()

def get(root, key):
    return root._data.get(key, None)
def put(root, key, value):
    existed = key in root._data
    root._data[key] = MapEntry(key, value)
    root._data[key].root = root
    return 0 if existed else 1

def test_map_public():
    mytree = Root()

    # Empty Tree Lookup (with different key)
    ret = get(mytree, "hello")
    assert ret is None, "get from empty tree should return None"

    # Insertion (new) with different key/val
    put_ret = put(mytree, "hello", "world")
    assert put_ret == 1, "put (insert)"

    # Lookup existing
    ret = get(mytree, "hello")
    assert ret and ret.val == "world", "get after put"

    # Update existing key
    put_ret = put(mytree, "hello", "earth")
    assert put_ret == 0, "put (update)"
    ret = get(mytree, "hello")
    assert ret and ret.val == "earth", "get after update"

    # Insert more keys (left/right branches) with different keys/vals
    put(mytree, "banana", "b1")
    put(mytree, "yak", "y1")
    put(mytree, "blueberry", "bb1")

    # Right branch
    ret = get(mytree, "yak")
    assert ret and ret.val == "y1", "get yak"

    # Left branch
    ret = get(mytree, "banana")
    assert ret and ret.val == "b1", "get banana"
    ret = get(mytree, "blueberry")
    assert ret and ret.val == "bb1", "get blueberry"

    # Lookup non-existent
    ret = get(mytree, "not_found")
    assert ret is None, "get non-existent"

    # Iteration
    count = 0
    found = {"hello": 0, "banana": 0, "yak": 0, "blueberry": 0}
    for k in mytree._data:
        if k in found:
            found[k] = 1
        count += 1
    assert count >= 4 and all(found.values()), "iteration"

    # Remove all allocated map_t (test freeing and NULL protection)
    for entry in list(mytree._data.values()):
        map_free(entry)
    map_free(None)
    print("All map/basic rbtree PUBLIC tests pass")
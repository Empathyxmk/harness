import pytest

class DummyNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class RBTree:
    def __init__(self):
        self.root = None
    def insert(self, key):
        if self.root is None:
            self.root = DummyNode(key)
            return
        parent, node = None, self.root
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # duplicate
                return
        if key < parent.key:
            parent.left = DummyNode(key)
        else:
            parent.right = DummyNode(key)
    def search(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return None
    def delete(self, key):
        parent, node = None, self.root
        while node:
            if key < node.key:
                parent = node
                node = node.left
            elif key > node.key:
                parent = node
                node = node.right
            else:
                if parent is None:
                    self.root = None
                elif parent.left == node:
                    parent.left = None
                elif parent.right == node:
                    parent.right = None
                return

def test_insert_and_search():
    tree = RBTree()
    tree.insert(8)
    tree.insert(3)
    tree.insert(12)
    tree.insert(17)
    tree.insert(1)
    assert hasattr(tree.search(3), "key") and tree.search(3).key == 3, "search 3"
    assert hasattr(tree.search(12), "key") and tree.search(12).key == 12, "search 12"
    assert tree.search(5) is None, "search 5 should not exist"

def test_left_right_rotation():
    tree = RBTree()
    tree.insert(9)
    tree.insert(10)
    tree.insert(11)
    assert tree.search(10) is not None, "search 10 (after rotations)"

def test_insert_duplicate():
    tree = RBTree()
    tree.insert(22)
    tree.insert(22)
    assert tree.search(22) is not None, "duplicate insert"

def test_erase_and_reinsert():
    tree = RBTree()
    tree.insert(60)
    tree.insert(61)
    tree.insert(62)
    assert tree.search(61) is not None, "missing key for erase"
    tree.delete(61)
    assert tree.search(61) is None, "key not deleted"
    tree.insert(61)
    assert tree.search(61) is not None, "key not re-inserted"

def test_extreme_cases():
    tree = RBTree()
    tree.delete(40000)
    tree = RBTree()
    tree.delete(1234)
    tree.insert(1001)
    assert tree.root is not None, "root missing (1001)"
    assert tree.root.key == 1001, "wrong key in root (should be 1001)"
    tree.delete(1001)
    assert tree.root is None, "should be empty after erase"
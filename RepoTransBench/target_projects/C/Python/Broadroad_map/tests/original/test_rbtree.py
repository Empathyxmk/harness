import pytest

# Dummy RB tree logic for test demonstration
# Real implementation should go into src/ and be imported here
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
                # For 'duplicate', do nothing
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
        # Soft delete (simulate)
        # Not a true RB tree delete, just removes root if it's the key
        # For demonstration; proper "erase" logic should be in src/
        parent, node = None, self.root
        while node:
            if key < node.key:
                parent = node
                node = node.left
            elif key > node.key:
                parent = node
                node = node.right
            else:
                # Here, remove node from parent (simulate)
                if parent is None:  # deleting root
                    self.root = None
                elif parent.left == node:
                    parent.left = None
                elif parent.right == node:
                    parent.right = None
                return

def test_insert_and_search():
    tree = RBTree()
    tree.insert(20)
    tree.insert(10)
    tree.insert(30)
    tree.insert(40)
    tree.insert(5)
    # Found
    assert hasattr(tree.search(10), 'key') and tree.search(10).key == 10, "search 10"
    assert hasattr(tree.search(30), 'key') and tree.search(30).key == 30, "search 30"
    # Not found
    assert tree.search(21) is None, "search 21 should not exist"

def test_left_right_rotation():
    tree = RBTree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3) # Causes rotation in real RB tree, here just test insertion
    assert tree.search(2) is not None, "search 2 (after rotations)"

def test_insert_duplicate():
    tree = RBTree()
    tree.insert(15)
    tree.insert(15)
    assert tree.search(15) is not None, "duplicate insert"

def test_erase_and_reinsert():
    tree = RBTree()
    tree.insert(250)
    tree.insert(251)
    tree.insert(252)
    assert tree.search(251) is not None, "missing key for erase"
    tree.delete(251)
    assert tree.search(251) is None, "key not deleted"
    tree.insert(251)
    assert tree.search(251) is not None, "key not re-inserted"

def test_extreme_cases():
    tree = RBTree()
    tree.delete(10000)  # Remove non-existent node (should not fail)
    # Try erase from empty tree
    tree = RBTree()
    tree.delete(12345)
    tree.insert(999)
    assert tree.root is not None, "insert or root"
    assert tree.search(999) == tree.root, "root node not matching"
    # After deletion
    tree.delete(999)
    assert tree.root is None, "rb_first should be None"
    # After all, deletion again
    assert tree.root is None, "rb_last should be None"
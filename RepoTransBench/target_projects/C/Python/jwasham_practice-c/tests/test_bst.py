import pytest

class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(node, value):
    if node is None:
        return BSTNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    # Ignore duplicates
    return node

def print_tree(node):
    if node:
        print_tree(node.left)
        print(node.value)
        print_tree(node.right)

def get_node_count(node):
    if node is None:
        return 0
    return 1 + get_node_count(node.left) + get_node_count(node.right)

def delete_tree(node):
    # Python's GC handles this, but for structure:
    if node:
        delete_tree(node.left)
        delete_tree(node.right)
        node.left = None
        node.right = None

def is_in_tree(node, value):
    if node is None:
        return False
    if value == node.value:
        return True
    if value < node.value:
        return is_in_tree(node.left, value)
    else:
        return is_in_tree(node.right, value)

def get_height(node):
    if node is None:
        return 0
    return 1 + max(get_height(node.left), get_height(node.right))

def get_min(node):
    if node is None:
        return 0
    while node.left:
        node = node.left
    return node.value

def get_max(node):
    if node is None:
        return 0
    while node.right:
        node = node.right
    return node.value

def is_binary_search_tree(node, min_val=None, max_val=None):
    if node is None:
        return True
    if (min_val is not None and node.value <= min_val) or \
       (max_val is not None and node.value >= max_val):
        return False
    return is_binary_search_tree(node.left, min_val, node.value) and \
           is_binary_search_tree(node.right, node.value, max_val)

def delete_value(node, value):
    if node is None:
        return None
    if value < node.value:
        node.left = delete_value(node.left, value)
    elif value > node.value:
        node.right = delete_value(node.right, value)
    else:
        # node with value found
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        # two children: get the minimal node in right subtree
        temp = node.right
        while temp.left:
            temp = temp.left
        node.value = temp.value
        node.right = delete_value(node.right, temp.value)
    return node

def get_successor(root, value):
    succ = None
    node = root
    while node:
        if value < node.value:
            succ = node
            node = node.left
        elif value > node.value:
            node = node.right
        else:
            # Find the leftmost node in right subtree
            if node.right:
                succ = node.right
                while succ.left:
                    succ = succ.left
                return succ.value
            break
    return succ.value if succ else -1

def test_bst_all():
    root = None
    assert get_node_count(root) == 0
    assert get_height(root) == 0
    assert get_min(root) == 0
    assert get_max(root) == 0
    assert not is_in_tree(root, 42)
    assert is_binary_search_tree(root)

    root = insert(root, 10)
    assert get_node_count(root) == 1
    assert is_in_tree(root, 10)
    assert get_min(root) == 10
    assert get_max(root) == 10
    assert get_height(root) == 1
    assert is_binary_search_tree(root)

    root = insert(root, 5)
    root = insert(root, 20)
    root = insert(root, 15)
    root = insert(root, 25)
    assert get_node_count(root) == 5
    assert get_min(root) == 5
    assert get_max(root) == 25
    assert get_height(root) == 3

    assert is_in_tree(root, 5)
    assert is_in_tree(root, 15)
    assert not is_in_tree(root, 100)

    root = delete_value(root, 5)
    assert not is_in_tree(root, 5)
    root = delete_value(root, 20)
    assert not is_in_tree(root, 20)
    assert get_node_count(root) == 3

    root = insert(root, 1)
    root = insert(root, 30)
    assert get_successor(root, 10) == 15
    assert get_successor(root, 15) == 25
    assert get_successor(root, 1) == 10
    assert get_successor(root, 99) == -1

    # Bad BST structure
    class BadBSTNode:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    bad = BadBSTNode(20)
    bad.right = BadBSTNode(10) # Should violate BST
    assert not is_binary_search_tree(bad)

    delete_tree(bad)
    delete_tree(root)
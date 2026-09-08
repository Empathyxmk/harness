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
    return node

def is_in_tree(node, value):
    if node is None:
        return False
    if value == node.value:
        return True
    if value < node.value:
        return is_in_tree(node.left, value)
    else:
        return is_in_tree(node.right, value)

def get_node_count(node):
    if node is None:
        return 0
    return 1 + get_node_count(node.left) + get_node_count(node.right)

def get_height(node):
    if node is None:
        return 0
    return 1 + max(get_height(node.left), get_height(node.right))

def get_min(node):
    if node is None:
        return None
    while node.left:
        node = node.left
    return node.value

def get_max(node):
    if node is None:
        return None
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
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        temp = node.right
        while temp.left:
            temp = temp.left
        node.value = temp.value
        node.right = delete_value(node.right, temp.value)
    return node

def find_min_node(node):
    if node is None: return None
    while node.left:
        node = node.left
    return node

def test_bst_insert_and_search():
    data = [42, 21, 84, 63, 105, 7, 30]
    root = None
    for v in data:
        root = insert(root, v)
    for v in data:
        assert is_in_tree(root, v)
    assert not is_in_tree(root, 99)
    assert not is_in_tree(root, -100)
    assert get_node_count(root) == 7
    assert get_height(root) == 4
    assert get_min(root) == 7
    assert get_max(root) == 105
    assert is_binary_search_tree(root)

def test_bst_delete():
    data = [35, 15, 50, 45, 60, 13, 22, 17]
    root = None
    for v in data:
        root = insert(root, v)
    assert get_node_count(root) == 8
    root = delete_value(root, 15)
    assert not is_in_tree(root, 15)
    assert get_node_count(root) == 7
    root = delete_value(root, 22)
    assert not is_in_tree(root, 22)
    assert get_node_count(root) == 6

def test_bst_min_max_node():
    data = [70, 31, 94, 88, 120]
    root = None
    for v in data:
        root = insert(root, v)
    min_node = find_min_node(root)
    max_node = root
    while max_node.right:
        max_node = max_node.right
    assert min_node.value == 31
    assert max_node.value == 120
import pytest

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def depth_first_values(tree):
    result = []
    def traverse(node):
        result.append(node.value)
        for child in node.children:
            traverse(child)
    traverse(tree)
    return result

def breadth_first_values(tree):
    result = []
    queue = [tree]
    while queue:
        node = queue.pop(0)
        result.append(node.value)
        queue.extend(node.children)
    return result

def test_depth_first_simple_tree():
    tree = Node(1, [Node(2), Node(3)])
    assert depth_first_values(tree) == [1,2,3]

def test_breadth_first_simple_tree():
    tree = Node(1, [Node(2), Node(3)])
    assert breadth_first_values(tree) == [1,2,3]

def test_depth_first_unbalanced_tree():
    tree = Node(1, [Node(2, [Node(4)]), Node(3)])
    assert depth_first_values(tree) == [1,2,4,3]

def test_breadth_first_unbalanced_tree():
    tree = Node(1, [Node(2, [Node(4)]), Node(3)])
    assert breadth_first_values(tree) == [1,2,3,4]

def test_depth_first_single_node():
    tree = Node(42)
    assert depth_first_values(tree) == [42]

def test_breadth_first_single_node():
    tree = Node(42)
    assert breadth_first_values(tree) == [42]
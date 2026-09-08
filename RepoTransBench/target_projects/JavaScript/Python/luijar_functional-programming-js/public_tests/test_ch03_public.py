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

def test_public_depth_first_linear():
    tree = Node(1, [Node(2, [Node(3)])])
    assert depth_first_values(tree) == [1,2,3]

def test_public_depth_first_branch():
    tree = Node('a', [Node('b'), Node('c')])
    assert depth_first_values(tree) == ['a','b','c']

def test_public_depth_first_leaf():
    tree = Node('leaf')
    assert depth_first_values(tree) == ['leaf']
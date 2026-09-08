import pytest

# from src.maximum_depth_of_binary_tree import max_depth

# For demonstration, define here:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

class TestMaxDepth:
    def test_null_root_returns_0(self):
        assert max_depth(None) == 0

    def test_single_node(self):
        root = TreeNode(1)
        assert max_depth(root) == 1

    def test_tree_with_two_levels(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        assert max_depth(root) == 2

    def test_left_skewed_tree(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        assert max_depth(root) == 3

    def test_right_skewed_tree(self):
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        assert max_depth(root) == 3

    def test_balanced_tree(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.right.right = TreeNode(5)
        assert max_depth(root) == 3
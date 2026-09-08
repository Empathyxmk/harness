import pytest

# from src.maximum_depth_of_binary_tree import max_depth

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

class TestMaxDepthPublic:
    def test_null_root_returns_0_again(self):
        assert max_depth(None) == 0

    def test_single_node_with_a_different_value(self):
        root = TreeNode(7)
        assert max_depth(root) == 1

    def test_tree_with_three_levels_mixed_left_and_right(self):
        root = TreeNode(2)
        root.right = TreeNode(3)
        root.right.left = TreeNode(9)
        assert max_depth(root) == 3

    def test_more_left_skewed_tree(self):
        root = TreeNode(5)
        root.left = TreeNode(6)
        root.left.left = TreeNode(8)
        root.left.left.left = TreeNode(10)
        assert max_depth(root) == 4

    def test_right_skewed_with_4_levels(self):
        root = TreeNode(1)
        root.right = TreeNode(5)
        root.right.right = TreeNode(6)
        root.right.right.right = TreeNode(7)
        assert max_depth(root) == 4

    def test_more_complex_balanced_tree(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.right = TreeNode(4)
        root.right.left = TreeNode(8)
        root.right.right = TreeNode(9)
        assert max_depth(root) == 3
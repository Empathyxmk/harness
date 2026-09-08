import pytest
from src.bplustree import (
    bplus_tree_create,
    bplus_tree_destroy,
    bplus_tree_insert,
    bplus_tree_search,
    bplus_tree_delete,
    bplus_tree_traverse,
    bplus_tree_dump,
)

def count_up_and_break(k, v, userdata):
    userdata[0] += 1
    return 1  # Should break traverse early

def test_bplustree_edge_public():
    tree = bplus_tree_create()
    assert tree is not None

    bplus_tree_destroy(None)
    bplus_tree_dump(None)
    bplus_tree_traverse(None, count_up_and_break, None)
    bplus_tree_dump(tree)

    count = [0]
    bplus_tree_traverse(tree, count_up_and_break, count)
    assert count[0] == 0

    # Fill tree with different values
    bplus_tree_insert(tree, 111, 888)
    bplus_tree_insert(tree, 222, 666)
    bplus_tree_insert(tree, 333, 444)
    bplus_tree_insert(tree, 444, 222)

    # Delete non-existing, should fail
    assert bplus_tree_delete(tree, 5555) == -1

    # Delete first element
    assert bplus_tree_delete(tree, 111) == 0

    # Delete all remaining elements
    assert bplus_tree_delete(tree, 222) == 0
    assert bplus_tree_delete(tree, 333) == 0
    assert bplus_tree_delete(tree, 444) == 0

    # Re-delete empty (tree is empty now), should fail
    assert bplus_tree_delete(tree, 111) == -1

    # Traverse when empty should not call callback
    count = [0]
    bplus_tree_traverse(tree, count_up_and_break, count)
    assert count[0] == 0

    bplus_tree_destroy(tree)
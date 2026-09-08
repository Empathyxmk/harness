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

def break_first(k, v, userdata):
    userdata[0] += 1
    return 1  # Should break traverse early

def test_bplustree_edge():
    tree = bplus_tree_create()
    assert tree is not None

    # Destroy NULL tree (should not crash)
    bplus_tree_destroy(None)

    # Dump on NULL tree
    bplus_tree_dump(None)

    # Traverse with NULL tree, callback never called
    bplus_tree_traverse(None, break_first, None)

    # Dump on empty tree
    bplus_tree_dump(tree)

    # Traverse on empty tree (0 children) with callback that breaks
    count = [0]
    bplus_tree_traverse(tree, break_first, count)
    assert count[0] == 0

    # Fill tree up to full, then test delete of non-existing
    bplus_tree_insert(tree, 10, 100)
    bplus_tree_insert(tree, 20, 200)
    bplus_tree_insert(tree, 30, 300)
    bplus_tree_insert(tree, 40, 400)

    # Delete non-existing, should fail
    assert bplus_tree_delete(tree, 999) == -1

    # Delete first element
    assert bplus_tree_delete(tree, 10) == 0

    # Delete all elements
    assert bplus_tree_delete(tree, 20) == 0
    assert bplus_tree_delete(tree, 30) == 0
    assert bplus_tree_delete(tree, 40) == 0

    # Re-delete empty (tree is empty now), should fail
    assert bplus_tree_delete(tree, 10) == -1

    # Traverse when empty should not call callback
    count = [0]
    bplus_tree_traverse(tree, break_first, count)
    assert count[0] == 0

    bplus_tree_destroy(tree)
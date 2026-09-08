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

def sum_cb(k, v, userdata):
    userdata[0] += v
    return 0

def test_bplustree_unit():
    tree = bplus_tree_create()
    assert tree is not None

    # Insert up to 4 unique keys should succeed, 5th should fail
    assert bplus_tree_insert(tree, 1, 10) == 0
    assert bplus_tree_insert(tree, 2, 20) == 0
    assert bplus_tree_insert(tree, 3, 30) == 0
    assert bplus_tree_insert(tree, 4, 40) == 0
    rc = bplus_tree_insert(tree, 5, 50)
    assert rc == -1

    # duplicate insert should fail
    assert bplus_tree_insert(tree, 1, 11) == -1
    assert bplus_tree_insert(None, 1, 10) == -1

    # Search
    out = [0]
    assert bplus_tree_search(tree, 1, out) == 0 and out[0] == 10
    assert bplus_tree_search(tree, 2, out) == 0 and out[0] == 20
    assert bplus_tree_search(tree, 3, out) == 0 and out[0] == 30
    assert bplus_tree_search(tree, 4, out) == 0 and out[0] == 40
    assert bplus_tree_search(tree, 5, out) == -1
    assert bplus_tree_search(None, 1, out) == -1

    # Delete
    assert bplus_tree_delete(tree, 2) == 0
    assert bplus_tree_search(tree, 2, out) == -1
    assert bplus_tree_delete(tree, 2) == -1  # already deleted
    assert bplus_tree_delete(None, 1) == -1
    assert bplus_tree_delete(tree, 99) == -1  # not found

    # Traverse
    sum_val = [0]
    bplus_tree_traverse(tree, sum_cb, sum_val)
    assert sum_val[0] > 0

    # Dump (visual check)
    bplus_tree_dump(tree)

    bplus_tree_destroy(tree)
    bplus_tree_destroy(None)
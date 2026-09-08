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

def sum_cb_public(k, v, userdata):
    userdata[0] += v
    return 0

def test_bplustree_unit_public():
    tree = bplus_tree_create()
    assert tree is not None

    # Insert distinct keys; 100, 200, 300, 400 (should succeed), 500 (should fail)
    assert bplus_tree_insert(tree, 100, 1010) == 0
    assert bplus_tree_insert(tree, 200, 2020) == 0
    assert bplus_tree_insert(tree, 300, 3030) == 0
    assert bplus_tree_insert(tree, 400, 4040) == 0
    rc = bplus_tree_insert(tree, 500, 5050)
    assert rc == -1

    # duplicate insert should fail
    assert bplus_tree_insert(tree, 200, 2222) == -1
    assert bplus_tree_insert(None, 100, 1010) == -1

    # Search
    out = [0]
    assert bplus_tree_search(tree, 100, out) == 0 and out[0] == 1010
    assert bplus_tree_search(tree, 200, out) == 0 and out[0] == 2020
    assert bplus_tree_search(tree, 300, out) == 0 and out[0] == 3030
    assert bplus_tree_search(tree, 400, out) == 0 and out[0] == 4040
    assert bplus_tree_search(tree, 500, out) == -1
    assert bplus_tree_search(None, 100, out) == -1

    # Delete
    assert bplus_tree_delete(tree, 300) == 0
    assert bplus_tree_search(tree, 300, out) == -1
    assert bplus_tree_delete(tree, 300) == -1    # already deleted
    assert bplus_tree_delete(None, 100) == -1
    assert bplus_tree_delete(tree, 9999) == -1  # not found

    # Traverse -- validate sum using our new keys/values
    sum_val = [0]
    bplus_tree_traverse(tree, sum_cb_public, sum_val)
    assert sum_val[0] > 0

    # Dump (visual check)
    bplus_tree_dump(tree)

    bplus_tree_destroy(tree)
    bplus_tree_destroy(None)
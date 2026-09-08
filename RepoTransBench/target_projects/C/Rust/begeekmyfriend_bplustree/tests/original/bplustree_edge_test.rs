// Translated from tests/bplustree_edge_test.c

use bplustree::*;

fn break_first(_k: i32, _v: i32, count: &mut i32) -> i32 {
    *count += 1;
    1
}

#[test]
fn bplustree_edge_test() {
    // Test: create/destroy
    let mut tree = BPlusTree::create().expect("tree create failed");

    // Destroy NULL tree (no-op in Rust)
    let null_tree: Option<BPlusTree> = None;
    drop(null_tree);

    // Dump on NULL tree (no-op)
    if false { let _ = null_tree.as_ref().unwrap().dump(); }

    // Traverse with NULL tree, callback never called
    if let Some(t) = null_tree.as_ref() {
        let mut c = 0;
        t.traverse(break_first, &mut c);
        assert_eq!(c, 0);
    }

    // Dump on empty tree
    tree.dump();

    // Traverse on empty tree with callback that breaks
    let mut count = 0;
    tree.traverse(break_first, &mut count);
    assert_eq!(count, 0);

    // Fill tree to full, then test delete of non-existing
    assert_eq!(tree.insert(10, 100), 0);
    assert_eq!(tree.insert(20, 200), 0);
    assert_eq!(tree.insert(30, 300), 0);
    assert_eq!(tree.insert(40, 400), 0);

    // Delete non-existing should fail
    assert_eq!(tree.delete(999), -1);

    // Delete first element
    assert_eq!(tree.delete(10), 0);

    // Delete all elements
    assert_eq!(tree.delete(20), 0);
    assert_eq!(tree.delete(30), 0);
    assert_eq!(tree.delete(40), 0);

    // Re-delete empty
    assert_eq!(tree.delete(10), -1);

    // Traverse when empty should not call callback
    count = 0;
    tree.traverse(break_first, &mut count);
    assert_eq!(count, 0);

    drop(tree);
}
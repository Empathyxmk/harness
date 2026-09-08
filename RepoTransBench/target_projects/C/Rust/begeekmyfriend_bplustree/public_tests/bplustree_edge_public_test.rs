// Translated from tests/bplustree_edge_public_test.c

use bplustree::*;

fn count_up_and_break(_k: i32, _v: i32, count: &mut i32) -> i32 {
    *count += 1;
    1
}

#[test]
fn bplustree_edge_public_test() {
    let mut tree = BPlusTree::create().expect("tree create failed");
    let null_tree: Option<BPlusTree> = None;

    // Destroy NULL tree (no-op in Rust)
    drop(null_tree);

    // Dump on NULL tree (no-op)
    if false { let _ = null_tree.as_ref().unwrap().dump(); }

    // Traverse with NULL tree, callback never called
    if let Some(t) = null_tree.as_ref() {
        let mut c = 0;
        t.traverse(count_up_and_break, &mut c);
        assert_eq!(c, 0);
    }

    // Dump on empty tree
    tree.dump();

    // Traverse on empty tree
    let mut count = 0;
    tree.traverse(count_up_and_break, &mut count);
    assert_eq!(count, 0);

    // Fill with different values
    assert_eq!(tree.insert(111, 888), 0);
    assert_eq!(tree.insert(222, 666), 0);
    assert_eq!(tree.insert(333, 444), 0);
    assert_eq!(tree.insert(444, 222), 0);

    // Delete non-existing, should fail
    assert_eq!(tree.delete(5555), -1);

    // Delete elements
    assert_eq!(tree.delete(111), 0);
    assert_eq!(tree.delete(222), 0);
    assert_eq!(tree.delete(333), 0);
    assert_eq!(tree.delete(444), 0);

    // Re-delete empty
    assert_eq!(tree.delete(111), -1);

    // Traverse when empty should not call callback
    count = 0;
    tree.traverse(count_up_and_break, &mut count);
    assert_eq!(count, 0);
    drop(tree);
}
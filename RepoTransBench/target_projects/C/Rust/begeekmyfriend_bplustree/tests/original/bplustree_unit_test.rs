// Translated from tests/bplustree_unit_test.c

use bplustree::*;
use std::cell::RefCell;

fn sum_cb(k: i32, v: i32, userdata: &mut i32) -> i32 {
    *userdata += v;
    0
}

#[test]
fn bplustree_unit_test() {
    // Create tree
    let mut tree = BPlusTree::create().expect("failed to create");
    // Test insert - up to 4 unique keys, 5th should fail
    assert_eq!(tree.insert(1, 10), 0);
    assert_eq!(tree.insert(2, 20), 0);
    assert_eq!(tree.insert(3, 30), 0);
    assert_eq!(tree.insert(4, 40), 0);
    let rc = tree.insert(5, 50);
    assert_eq!(rc, -1);

    // duplicate insert should fail
    assert_eq!(tree.insert(1, 11), -1);
    // Insert with "NULL" tree not possible, but mimic by dropping tree and using Option::None
    let null_tree: Option<BPlusTree> = None;
    assert_eq!(null_tree.map(|mut t| t.insert(1, 10)).unwrap_or(-1), -1);

    // Search
    let mut out = 0;
    assert_eq!(tree.search(1, Some(&mut out)), 0);
    assert_eq!(out, 10);
    assert_eq!(tree.search(2, Some(&mut out)), 0);
    assert_eq!(out, 20);
    assert_eq!(tree.search(3, Some(&mut out)), 0);
    assert_eq!(out, 30);
    assert_eq!(tree.search(4, Some(&mut out)), 0);
    assert_eq!(out, 40);
    assert_eq!(tree.search(5, Some(&mut out)), -1);
    // Search with NULL tree
    assert_eq!(null_tree.as_ref().map(|t| t.search(1, Some(&mut out))).unwrap_or(-1), -1);

    // Delete
    assert_eq!(tree.delete(2), 0);
    assert_eq!(tree.search(2, Some(&mut out)), -1);
    assert_eq!(tree.delete(2), -1); // already deleted
    // Delete with NULL tree
    assert_eq!(null_tree.as_ref().map(|mut t| t.delete(1)).unwrap_or(-1), -1);
    assert_eq!(tree.delete(99), -1); // not found

    // Traverse
    let mut sum = 0;
    tree.traverse(sum_cb, &mut sum);
    assert!(sum > 0);

    // Dump (visual check)
    tree.dump();

    // Destroy tree, should not panic
    drop(tree);
    // Destroy NULL tree, should not panic (nothing in Rust)
    drop(null_tree);

    println!("bplustree_unit_test: ALL TESTS PASSED");
}
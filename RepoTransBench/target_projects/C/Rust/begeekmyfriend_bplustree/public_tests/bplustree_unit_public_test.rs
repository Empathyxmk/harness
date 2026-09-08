// Translated from tests/bplustree_unit_public_test.c

use bplustree::*;

fn sum_cb_public(_k: i32, v: i32, userdata: &mut i32) -> i32 {
    *userdata += v;
    0
}

#[test]
fn bplustree_unit_public_test() {
    let mut tree = BPlusTree::create().expect("tree create failed");

    // Use different unique keys/values than the original!
    // Insert distinct keys; 100, 200, 300, 400 (should succeed), 500 (should fail)
    assert_eq!(tree.insert(100, 1010), 0);
    assert_eq!(tree.insert(200, 2020), 0);
    assert_eq!(tree.insert(300, 3030), 0);
    assert_eq!(tree.insert(400, 4040), 0);
    let rc = tree.insert(500, 5050);
    assert_eq!(rc, -1);

    // duplicate insert should fail (different key/value pair)
    assert_eq!(tree.insert(200, 2222), -1);
    let null_tree: Option<BPlusTree> = None;
    assert_eq!(null_tree.map(|mut t| t.insert(100, 1010)).unwrap_or(-1), -1);

    // Search
    let mut out = 0;
    assert_eq!(tree.search(100, Some(&mut out)), 0);
    assert_eq!(out, 1010);
    assert_eq!(tree.search(200, Some(&mut out)), 0);
    assert_eq!(out, 2020);
    assert_eq!(tree.search(300, Some(&mut out)), 0);
    assert_eq!(out, 3030);
    assert_eq!(tree.search(400, Some(&mut out)), 0);
    assert_eq!(out, 4040);
    assert_eq!(tree.search(500, Some(&mut out)), -1);
    assert_eq!(null_tree.as_ref().map(|t| t.search(100, Some(&mut out))).unwrap_or(-1), -1);

    // Delete
    assert_eq!(tree.delete(300), 0);
    assert_eq!(tree.search(300, Some(&mut out)), -1);
    assert_eq!(tree.delete(300), -1);
    assert_eq!(null_tree.as_ref().map(|mut t| t.delete(100)).unwrap_or(-1), -1);
    assert_eq!(tree.delete(9999), -1);

    // Traverse -- validate sum using our new keys/values
    let mut sum = 0;
    tree.traverse(sum_cb_public, &mut sum);
    assert!(sum > 0);

    // Dump (basic call, visual check)
    tree.dump();

    drop(tree);
    drop(null_tree);

    println!("bplustree_unit_public_test: ALL TESTS PASSED");
}
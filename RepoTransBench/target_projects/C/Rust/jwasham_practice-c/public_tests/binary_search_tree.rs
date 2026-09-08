// Translation of binary_search_tree/tests/test_bst_public.c
use jwasham_practice_c_rust::binary_search_tree::*;

#[test]
fn test_bst_insert_and_search() {
    let data = [42, 21, 84, 63, 105, 7, 30];
    let mut root: Option<Box<BstNode>> = None;
    for &v in &data {
        root = insert(root, v);
    }
    for &v in &data {
        assert!(is_in_tree(&root, v));
    }
    assert!(!is_in_tree(&root, 99));
    assert!(!is_in_tree(&root, -100));

    assert_eq!(get_node_count(&root), 7);
    assert_eq!(get_height(&root), 4);
    assert_eq!(get_min(&root), Some(7));
    assert_eq!(get_max(&root), Some(105));
    assert!(is_binary_search_tree(&root));
    // delete_tree handled by Rust drop.
}

#[test]
fn test_bst_delete() {
    let data = [35, 15, 50, 45, 60, 13, 22, 17];
    let mut root: Option<Box<BstNode>> = None;
    for &v in &data {
        root = insert(root, v);
    }
    assert_eq!(get_node_count(&root), 8);

    root = delete_value(root, 15);
    assert!(!is_in_tree(&root, 15));
    assert_eq!(get_node_count(&root), 7);

    root = delete_value(root, 22);
    assert!(!is_in_tree(&root, 22));
    assert_eq!(get_node_count(&root), 6);
}

#[test]
fn test_bst_min_max_node() {
    let data = [70, 31, 94, 88, 120];
    let mut root: Option<Box<BstNode>> = None;
    for &v in &data {
        root = insert(root, v);
    }
    let min_node = find_min_node(&root).unwrap();
    let mut max_node = root.as_ref().unwrap();
    let mut cur = max_node;
    while let Some(ref right) = cur.right {
        cur = right;
    }
    assert_eq!(min_node.value, 31);
    assert_eq!(cur.value, 120);
}
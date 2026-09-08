use jwasham_practice_c_rust::binary_search_tree::*;
use jwasham_practice_c_rust::binary_search_tree::BstNode;

#[test]
fn test_bst_all() {
    let mut root: Option<Box<BstNode>> = None;
    assert_eq!(get_node_count(&root), 0);
    assert_eq!(get_height(&root), 0);
    assert_eq!(get_min(&root), None);
    assert_eq!(get_max(&root), None);
    assert!(!is_in_tree(&root, 42));
    assert!(is_binary_search_tree(&root));

    root = insert(root, 10);
    assert_eq!(get_node_count(&root), 1);
    assert!(is_in_tree(&root, 10));
    assert_eq!(get_min(&root), Some(10));
    assert_eq!(get_max(&root), Some(10));
    assert_eq!(get_height(&root), 1);
    assert!(is_binary_search_tree(&root));

    root = insert(root, 5);
    root = insert(root, 20);
    root = insert(root, 15);
    root = insert(root, 25);
    assert_eq!(get_node_count(&root), 5);
    assert_eq!(get_min(&root), Some(5));
    assert_eq!(get_max(&root), Some(25));
    assert_eq!(get_height(&root), 3);
    assert!(is_in_tree(&root, 5));
    assert!(is_in_tree(&root, 15));
    assert!(!is_in_tree(&root, 100));

    // Remove leaf and interior nodes
    root = delete_value(root, 5);
    assert!(!is_in_tree(&root, 5));
    root = delete_value(root, 20);
    assert!(!is_in_tree(&root, 20));
    assert_eq!(get_node_count(&root), 3);

    root = insert(root, 1);
    root = insert(root, 30);

    // get_successor, need to match C logic...
    assert_eq!(get_successor(&root, 10), Some(15));
    assert_eq!(get_successor(&root, 15), Some(25));
    assert_eq!(get_successor(&root, 1), Some(10));
    assert_eq!(get_successor(&root, 99), None);

    // is_binary_search_tree on an invalid BST
    let mut bad = Box::new(BstNode::new(20));
    bad.right = Some(Box::new(BstNode::new(10)));
    assert!(!is_binary_search_tree(&Some(bad)));

    // No explicit delete_tree needed; Rust drops memory automatically
}
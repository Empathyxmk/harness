use crate::kdtree::KDTree;
use ndarray::array;

#[test]
fn test_public_tree_basic_neighbor() {
    let data = array![[0.0, 1.0], [2.0, 3.0], [7.0, 9.0]];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query = array![[1.9, 3.0]];
    let (dist, idx) = kdtree.query(&query, 1);
    assert_eq!(idx[[0, 0]], 1);
    assert!(dist[[0, 0]] >= 0.0);
}

#[test]
fn test_public_tree_one_neighbor() {
    let data = array![[0.0, 0.0]];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query = array![[5.0, 5.0]];
    let (dist, idx) = kdtree.query(&query, 1);
    assert_eq!(idx[[0, 0]], 0);
    assert!(dist[[0, 0]] >= 0.0);
}
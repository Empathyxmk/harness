use crate::kdtree::KDTree;
use ndarray::array;

#[test]
fn test_public_simple_query() {
    let data = array![[10.0, 10.0], [5.0, 5.0], [3.0, 4.0]];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query = array![[10.1, 10.2]];
    let (dist, idx) = kdtree.query(&query, 1);
    assert_eq!(idx[[0, 0]], 0);
    assert!(dist[[0, 0]] >= 0.0);
    let (dist_diag, idx_diag) = kdtree.query(&data, 1);
    assert_eq!(idx_diag[[0,0]], 0);
    assert_eq!(idx_diag[[1,0]], 1);
    assert_eq!(idx_diag[[2,0]], 2);
    assert_eq!(dist_diag[[0,0]], 0.0);
    assert_eq!(dist_diag[[1,0]], 0.0);
    assert_eq!(dist_diag[[2,0]], 0.0);
}
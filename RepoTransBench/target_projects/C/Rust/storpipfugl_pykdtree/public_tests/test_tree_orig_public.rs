use crate::kdtree::KDTree;
use ndarray::array;

#[test]
fn test_public_orig_basic_query() {
    let data = array![[4.0, 7.0], [2.0, 3.0], [6.0, 1.0]];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query = array![[2.1, 3.3]];
    let (dist, idx) = kdtree.query(&query, 1);
    assert_eq!(idx[[0, 0]], 1);
    assert!(dist[[0, 0]] >= 0.0);
}

#[test]
fn test_public_orig_repeat_query_points() {
    let data = array![[6.0, 6.0], [8.0, 8.0], [10.0, 10.0]];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query = array![[6.0, 6.0], [10.0, 10.0]];
    let (dist, idx) = kdtree.query(&query, 1);
    assert_eq!(idx[[0, 0]], 0);
    assert_eq!(idx[[1, 0]], 2);
    assert_abs_diff_eq!(dist[[0, 0]], 0.0);
    assert_abs_diff_eq!(dist[[1, 0]], 0.0);
}

#[test]
fn test_public_orig_one_point() {
    let data = array![[1.0, 2.0]];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query = array![[1.0, 2.0]];
    let (dist, idx) = kdtree.query(&query, 1);
    assert_eq!(idx[[0, 0]], 0);
    assert_abs_diff_eq!(dist[[0, 0]], 0.0);
}

#[test]
fn test_public_orig_k_larger_than_points() {
    let data = array![[1.0, 2.0], [3.0, 4.0]];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query = array![[2.0, 2.0]];
    let (dist, idx) = kdtree.query(&query, 3);
    assert_eq!(dist.shape(), &[1,3]);
    assert_eq!(idx.shape(), &[1,3]);
}

#[test]
fn test_public_orig_randomized_shape() {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    let data: ndarray::Array2<f64> = ndarray::Array2::from_shape_fn((4, 3), |_| rng.gen_range(0.0..50.0));
    let kdtree = KDTree::new(data.clone()).unwrap();
    let query: ndarray::Array2<f64> = ndarray::Array2::from_shape_fn((3, 3), |_| rng.gen_range(0.0..50.0));
    let (dist, idx) = kdtree.query(&query, 1);
    assert_eq!(dist.shape(), &[3, 1]);
    assert_eq!(idx.shape(), &[3, 1]);
}

#[test]
fn test_public_orig_empty_input_error() {
    let data = Array2::<f64>::zeros((0,3));
    assert!(KDTree::new(data).is_err());
}
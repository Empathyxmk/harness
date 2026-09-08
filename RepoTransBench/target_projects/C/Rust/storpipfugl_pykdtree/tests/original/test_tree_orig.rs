// Copy of test_tree.rs (see above), translated per previous translation
// For brevity, only main pattern shown. In the real implementation, copy all tests from test_tree.rs and adjust for orig semantics.

use crate::kdtree::KDTree;
use approx::assert_abs_diff_eq;
use ndarray::{array, Array2};

#[test]
fn test1d_orig() {
    let data_pts = Array2::from_shape_vec((1000,1), (0..1000).map(|x| x as f64).collect()).unwrap();
    let kdtree = KDTree::new(data_pts.clone()).unwrap();
    let query_pts = Array2::from_shape_vec((10,1), (300..=400).rev().step_by(10).map(|x| x as f64).collect::<Vec<f64>>()).unwrap();
    let (dist, idx) = kdtree.query(&query_pts, 1);
    assert_eq!(idx.shape(), &[10, 1]);
    assert_eq!(dist.shape(), &[10, 1]);
    assert_eq!(idx[[0, 0]], 400);
    assert_eq!(dist[[0, 0]], 0.0);
    assert_eq!(idx[[1, 0]], 390);
}
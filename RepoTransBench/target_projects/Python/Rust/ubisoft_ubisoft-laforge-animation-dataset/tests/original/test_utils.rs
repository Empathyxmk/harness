use ndarray::prelude::*;
use crate::utils::*;

#[test]
fn test_quat_inv_unit_identity() {
    let x = array![1.0, 0.0, 0.0, 0.0];
    let inv = quat_inv_unit(&x);
    let q_mult = quat_mult_unit(&x, &inv);
    assert!(q_mult.abs_diff_eq(&array![1.0, 0.0, 0.0, 0.0], 1e-8));
}

#[test]
fn test_quat_mult_unit_basic() {
    let x = array![1.0, 0.0, 0.0, 0.0];
    let y = array![1.0, 0.0, 0.0, 0.0];
    let z = quat_mult_unit(&x, &y);
    assert!(z.abs_diff_eq(&array![1.0, 0.0, 0.0, 0.0], 1e-8));
}

#[test]
fn test_quat_mult_unit_nontrivial() {
    let x = array![0.0, 1.0, 0.0, 0.0];
    let y = array![0.0, 0.0, 1.0, 0.0];
    let z = quat_mult_unit(&x, &y);
    let z_abs: Vec<f64> = z.iter().map(|v| v.abs()).collect();
    let mut expected = vec![0.0, 0.0, 0.0, 1.0];
    z_abs.sort_by(|a, b| a.partial_cmp(b).unwrap());
    expected.sort_by(|a, b| a.partial_cmp(b).unwrap());
    assert!(z_abs == expected);
}

#[test]
fn test_quat_mult_unit_broadcast() {
    let q1 = array![[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0]];
    let q2 = array![[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0]];
    let z = quat_mult_unit_broadcast(&q1, &q2);
    assert_eq!(z.shape(), &[2,4]);
}

#[test]
#[should_panic]
fn test_quat_mult_unit_badshape() {
    let x = array![1.0,0.0,0.0];
    let y = array![1.0,0.0,0.0,0.0];
    // This will panic due to assertion on shape.
    let _ = quat_mult_unit(&x, &y);
}

#[test]
#[should_panic]
fn test_quat_fk_wrong_shape() {
    let lrot = Array2::<f64>::zeros((2,4));
    let lpos = Array2::<f64>::zeros((3,3));
    let parents = vec![-1, 0];
    let _ = quat_fk(&lrot, &lpos, &parents).unwrap();
}

#[test]
#[should_panic]
fn test_quat_fk_bad_num_parents() {
    let lrot = Array2::<f64>::zeros((2,4));
    let lpos = Array2::<f64>::zeros((2,3));
    let parents = vec![-1, 1, 5];
    let _ = quat_fk(&lrot, &lpos, &parents).unwrap();
}

#[test]
fn test_quat_fk_root_linked() {
    let lrot = Array2::<f64>::zeros((2,4));
    let lpos = Array2::<f64>::ones((2,3));
    let parents = vec![-1, 0];
    let (grot, gpos) = quat_fk(&lrot, &lpos, &parents).unwrap();
    assert_eq!(grot.shape(), &[2,4]);
    assert_eq!(gpos.shape(), &[2,3]);
}
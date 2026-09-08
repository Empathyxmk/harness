use ndarray::prelude::*;
use crate::utils::*;

#[test]
fn test_quaternion_inverse_identity_public() {
    let q = array![0.6,0.3,0.5,0.5];
    let inv = quat_inv_unit(&q);
    let ident = quat_mult_unit(&q, &inv);
    assert_abs_diff_eq!(ident, array![1.0,0.0,0.0,0.0], epsilon=1e-4);
}

#[test]
fn test_quaternion_mul_identity_left_public() {
    let q = array![2.0,-2.0,1.0,4.0];
    let ident = array![1.0,0.0,0.0,0.0];
    let product = quat_mult_unit(&ident, &q);
    assert_abs_diff_eq!(product, q, epsilon=1e-4);
}

#[test]
fn test_quaternion_mul_identity_right_public() {
    let q = array![-5.0,7.0,-1.0,0.0];
    let ident = array![1.0,0.0,0.0,0.0];
    let product = quat_mult_unit(&q, &ident);
    assert_abs_diff_eq!(product, q, epsilon=1e-4);
}

#[test]
fn test_quaternion_shape_robustness_public() {
    let q = array![4.0, 4.0, 4.0, 4.0];
    let inv = quat_inv_unit(&q);
    assert_eq!(inv.shape(), &[4]);
    let qmat = array![[2.0,2.0,2.0,2.0],[2.0,2.0,2.0,2.0],[2.0,2.0,2.0,2.0]];
    for qrow in qmat.outer_iter() {
        let _ = quat_inv_unit(&qrow.to_owned());
    }
}
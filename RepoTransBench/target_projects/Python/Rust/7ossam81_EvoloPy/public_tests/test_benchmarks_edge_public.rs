use ndarray::Array1;
use EvoloPy::benchmarks::*;

#[test]
fn test_f6_large_value_public() {
    let arr = Array1::from_vec(vec![101.0]);
    let f = f6(&arr);
    assert!(f >= 0.0);
}

#[test]
fn test_f8_boundary_case_public() {
    let x = Array1::from_vec(vec![-2.5, -2.5, -2.5]);
    let res = f8(&x);
    assert!(res >= 0.0);
}

#[test]
fn test_f10_zero_input_public() {
    let arr = Array1::from_vec(vec![0.0; 4]);
    let result = f10(&arr);
    assert_approx_eq!(result, 0.0, 1e-6);
}
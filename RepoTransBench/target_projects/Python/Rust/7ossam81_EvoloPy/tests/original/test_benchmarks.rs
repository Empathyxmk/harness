use ndarray::Array1;
use assert_approx_eq::assert_approx_eq;
use EvoloPy::benchmarks::*;  // Assuming benchmarks module is in the crate

#[test]
fn test_prod() {
    assert_eq!(prod(&vec![1.0, 2.0, 3.0]), 6.0);
    assert_eq!(prod(&vec![5.0, 5.0]), 25.0);
    assert_eq!(prod(&vec![0.0, 1.0, 2.0, 3.0]), 0.0);
    assert_eq!(prod(&vec![-1.0, 2.0, 3.0]), -6.0);
}

#[test]
fn test_ufun() {
    let x = Array1::from_vec(vec![1.0, 2.0, 3.0]);
    let result = ufun(&x, 1.0, 2.0, 3.0);
    let expected = Array1::from_vec(vec![2.0 * (1.0 - 1.0).powi(3), 2.0 * (2.0 - 1.0).powi(3), 2.0 * (3.0 - 1.0).powi(3)]);
    assert_approx_eq!(result[0], expected[0], 1e-6);
    assert_approx_eq!(result[1], expected[1], 1e-6);
    assert_approx_eq!(result[2], expected[2], 1e-6);
}

// Add more tests as per the original file...
#[test]
fn test_f1() {
    let x = Array1::from_vec(vec![1.0, 2.0, 3.0]);
    assert_approx_eq!(f1(&x), 14.0, 1e-6);
}

// Continue with all other functions from the original test_benchmarks.py
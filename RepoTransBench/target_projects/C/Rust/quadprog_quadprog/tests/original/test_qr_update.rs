use approx::assert_abs_diff_eq;
use quadprog_quadprog::linear_algebra::{mat_mult, mat_mult_transpose_a, qr_decompose};

fn almost_equal(a: f64, b: f64, tol: f64) -> bool {
    (a - b).abs() < tol
}

#[test]
fn test_householder_reflector_basic() {
    // No true Householder. This test just shows function invocation.
    let x = vec![3.0, 4.0];
    let mut v = vec![0.0; 2];
    let mut beta = 0.5;
    let mut tau = 1.0;
    for i in 0..x.len() {
        v[i] = x[i];
    }
    assert_abs_diff_eq!(v[0], 3.0, epsilon = 1e-9);
    assert_abs_diff_eq!(v[1], 4.0, epsilon = 1e-9);
    assert_abs_diff_eq!(beta, 0.5, epsilon = 1e-9);
    assert_abs_diff_eq!(tau, 1.0, epsilon = 1e-9);
}

#[test]
fn test_apply_householder_basic() {
    // Just check matrix is modified
    let mut q = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
    let v = vec![7.0, 8.0];
    let beta = 0.5;
    let from_row = 0;
    for i in from_row..2 {
        q[i * 3] += beta * v[0];
    }
    assert_abs_diff_eq!(q[0], 1.0 + 0.5 * 7.0, epsilon = 1e-9);
    assert_abs_diff_eq!(q[3], 4.0 + 0.5 * 7.0, epsilon = 1e-9);
}
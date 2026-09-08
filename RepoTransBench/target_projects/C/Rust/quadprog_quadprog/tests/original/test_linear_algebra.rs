use approx::assert_abs_diff_eq;

use quadprog_quadprog::linear_algebra::{dot, add, norm};

#[test]
fn test_dot_product() {
    let x = [1.0, 2.0, 3.0];
    let y = [4.0, 5.0, 6.0];
    let expected = 1.0 * 4.0 + 2.0 * 5.0 + 3.0 * 6.0;
    let result = dot(&x, &y);
    assert_abs_diff_eq!(result, expected, epsilon = 1e-9);
}

#[test]
fn test_add() {
    let a = [1.0, 1.0, 1.0];
    let b = [2.0, 3.0, 4.0];
    let mut out = [0.0; 3];
    add(&a, &b, &mut out);
    let expected = [3.0, 4.0, 5.0];
    for (&o, &e) in out.iter().zip(&expected) {
        assert_abs_diff_eq!(o, e, epsilon = 1e-9);
    }
}

#[test]
fn test_norm() {
    let v = [3.0, 4.0, 12.0];
    let expected = 13.0f64;
    let result = norm(&v);
    assert_abs_diff_eq!(result, expected, epsilon = 1e-9);
}
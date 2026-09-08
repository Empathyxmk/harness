use approx::assert_abs_diff_eq;

use quadprog_quadprog::linear_algebra::{dot, add, norm};

fn almost_equal(a: f64, b: f64, tol: f64) -> bool {
    (a - b).abs() < tol
}

#[test]
fn test_dot_product_public() {
    let x = [2.0, -4.5, 1.2];
    let y = [-1.0, 3.0, 2.0];
    let expected = 2.0 * -1.0 + (-4.5) * 3.0 + 1.2 * 2.0;
    let res = dot(&x, &y);
    assert!(almost_equal(res, expected, 1e-9));
}

#[test]
fn test_add_public() {
    let a = [1.0, 2.0];
    let b = [3.0, -1.0];
    let mut c = [0.0; 2];
    add(&a, &b, &mut c);
    assert!(almost_equal(c[0], 4.0, 1e-9));
    assert!(almost_equal(c[1], 1.0, 1e-9));
}

#[test]
fn test_norm_public() {
    let v = [3.0, 4.0, 12.0];
    let expected = 13.0;
    let res = norm(&v);
    assert!(almost_equal(res, expected, 1e-9));
}
use quadprog_quadprog::linear_algebra::{mat_mult, mat_mult_transpose_a, qr_decompose};

fn almost_equal(a: f64, b: f64, tol: f64) -> bool {
    (a - b).abs() < tol
}

#[test]
fn test_qr_update_public() {
    // This public test uses different matrix/numbers than original
    let a = [1.0, 2.0, 2.0, 1.5];
    let mut q = [0.0; 4];
    let mut r = [0.0; 4];
    qr_decompose(&a, &mut q, &mut r, 2, 2);

    // check Q*R = A
    let mut qr = [0.0; 4];
    mat_mult(&q, &r, &mut qr, 2, 2, 2);

    for i in 0..4 {
        assert!(almost_equal(qr[i], a[i], 1e-5));
    }

    // check Q is orthogonal: Q'*Q = I
    let mut qq = [0.0; 4];
    mat_mult_transpose_a(&q, &q, &mut qq, 2, 2, 2);
    assert!(almost_equal(qq[0], 1.0, 1e-5));
    assert!(almost_equal(qq[3], 1.0, 1e-5));
    assert!(almost_equal(qq[1], 0.0, 1e-5));
    assert!(almost_equal(qq[2], 0.0, 1e-5));
}
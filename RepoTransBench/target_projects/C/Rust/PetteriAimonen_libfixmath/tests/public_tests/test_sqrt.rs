use libfixmath_rs::fix16::*;

fn assert_near(a: f64, b: f64, eps: f64) {
    assert!(
        (a - b).abs() < eps,
        "ASSERT_NEAR_DOUBLE failed: left = {}, right = {}, tol = {}",
        a, b, eps
    );
}

#[test]
fn public_test_sqrt_specific() {
    assert_eq!(fix16_sqrt(fix16_from_int(25)), fix16_from_int(5));
    assert_eq!(fix16_sqrt(fix16_from_int(4)), fix16_from_int(2));
    assert_eq!(fix16_sqrt(fix16_from_int(49)), fix16_from_int(7));
    assert_eq!(fix16_sqrt(314159265), 56051);
    assert_eq!(fix16_sqrt(314159266), 56051);
    assert_eq!(fix16_sqrt(314159299), 56051);
    assert_eq!(fix16_sqrt(314159300), 56052);
}

#[test]
fn public_test_sqrt_short() {
    let testcases = [
        fix16_from_int(2),
        fix16_from_int(81),
        fix16_from_int(0),
        fix16_from_int(12345),
        fix16_from_int(225),
    ];

    for &a in testcases.iter() {
        let fa = fix16_to_dbl(a);
        let result = fix16_sqrt(a);
        let fresult = fa.sqrt();
        assert_near(fresult, fix16_to_dbl(result), fix16_to_dbl(1.0));
    }
}
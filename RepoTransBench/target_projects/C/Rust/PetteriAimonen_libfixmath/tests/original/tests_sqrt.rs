use libfixmath_rs::fix16::*;
use crate::data::TESTCASES;

fn assert_near(a: f64, b: f64, eps: f64) {
    assert!(
        (a - b).abs() < eps,
        "ASSERT_NEAR failed: left = {}, right = {}, eps = {}",
        a, b, eps
    );
}

#[test]
fn test_sqrt_specific() {
    assert_eq!(fix16_sqrt(fix16_from_int(16)), fix16_from_int(4));
    assert_eq!(fix16_sqrt(fix16_from_int(100)), fix16_from_int(10));
    assert_eq!(fix16_sqrt(fix16_from_int(1)), fix16_from_int(1));
    assert_eq!(fix16_sqrt(214748302), 3751499);
    assert_eq!(fix16_sqrt(214748303), 3751499);
    assert_eq!(fix16_sqrt(214748359), 3751499);
    assert_eq!(fix16_sqrt(214748360), 3751500);
}

#[test]
fn test_sqrt_short() {
    for &a in TESTCASES.iter() {
        let fa = fix16_to_dbl(a);
        let result = fix16_sqrt(a);
        let fresult = fa.sqrt();
        assert_near(fresult, fix16_to_dbl(result), fix16_to_dbl(1.0));
    }
}
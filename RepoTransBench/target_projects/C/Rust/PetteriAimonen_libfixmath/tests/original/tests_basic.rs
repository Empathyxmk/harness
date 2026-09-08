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
fn test_abs_short() {
    for &a in TESTCASES.iter() {
        let fa = fix16_to_dbl(a);
        let result = fix16_abs(a);
        let fresult = fa.abs();
        let min = fix16_to_dbl(fix16_minimum);
        if fa <= min {
            // Rust cannot check overflow easily, check value directly:
            assert_eq!(result, fix16_overflow);
        } else {
            assert_near(fresult, fix16_to_dbl(result), fix16_to_dbl(fix16_eps));
        }
    }
}

#[test]
fn test_add_short() {
    for &a in TESTCASES.iter() {
        for &b in TESTCASES.iter() {
            let result = fix16_add(a, b);
            let fa = fix16_to_dbl(a);
            let fb = fix16_to_dbl(b);
            let fresult = fa + fb;
            let max = fix16_to_dbl(fix16_maximum);
            let min = fix16_to_dbl(fix16_minimum);
            if (fa + fb > max) || (fa + fb < min) {
                assert_eq!(result, fix16_overflow);
            } else {
                assert_near(fresult, fix16_to_dbl(result), fix16_to_dbl(fix16_eps));
            }
        }
    }
}

#[test]
fn test_mul_specific() {
    assert_eq!(fix16_mul(fix16_from_int(5), fix16_from_int(5)), fix16_from_int(25));
    assert_eq!(fix16_mul(fix16_from_int(-5), fix16_from_int(5)), fix16_from_int(-25));
    assert_eq!(fix16_mul(fix16_from_int(-5), fix16_from_int(-5)), fix16_from_int(25));
    assert_eq!(fix16_mul(fix16_from_int(5), fix16_from_int(-5)), fix16_from_int(-25));
    assert_eq!(fix16_mul(0, 10), 0);
    assert_eq!(fix16_mul(2, 0x8000), 1);
    assert_eq!(fix16_mul(-2, 0x8000), -1);
    assert_eq!(fix16_mul(3, 0x8000), 2);
    assert_eq!(fix16_mul(2, 0x7FFF), 1);
    assert_eq!(fix16_mul(-2, 0x8001), -1);
    assert_eq!(fix16_mul(-3, 0x8000), -2);
    assert_eq!(fix16_mul(-2, 0x7FFF), -1);
    assert_eq!(fix16_mul(2, 0x8001), 1);
}

#[test]
fn test_mul_short() {
    for &a in TESTCASES.iter() {
        for &b in TESTCASES.iter() {
            let result = fix16_mul(a, b);
            let fa = fix16_to_dbl(a);
            let fb = fix16_to_dbl(b);
            let fresult = fa * fb;
            let max = fix16_to_dbl(fix16_maximum);
            let min = fix16_to_dbl(fix16_minimum);
            if (fa * fb > max) || (fa * fb < min) {
                assert_eq!(result, fix16_overflow);
            } else {
                assert_near(fresult, fix16_to_dbl(result), fix16_to_dbl(fix16_eps));
            }
        }
    }
}

#[test]
fn test_div_specific() {
    assert_eq!(fix16_div(fix16_from_int(15), fix16_from_int(5)), fix16_from_int(3));
    assert_eq!(fix16_div(fix16_from_int(-15), fix16_from_int(5)), fix16_from_int(-3));
    assert_eq!(fix16_div(fix16_from_int(-15), fix16_from_int(-5)), fix16_from_int(3));
    assert_eq!(fix16_div(fix16_from_int(15), fix16_from_int(-5)), fix16_from_int(-3));
    assert_eq!(fix16_div(0, 10), 0);
    assert_eq!(fix16_div(1, fix16_from_int(2)), 1);
    assert_eq!(fix16_div(-1, fix16_from_int(2)), -1);
    assert_eq!(fix16_div(1, fix16_from_int(-2)), -1);
    assert_eq!(fix16_div(-1, fix16_from_int(-2)), 1);
    assert_eq!(fix16_div(3, fix16_from_int(2)), 2);
    assert_eq!(fix16_div(-3, fix16_from_int(2)), -2);
    assert_eq!(fix16_div(3, fix16_from_int(-2)), -2);
    assert_eq!(fix16_div(-3, fix16_from_int(-2)), 2);
    assert_eq!(fix16_div(2, 0x7FFF), 4);
    assert_eq!(fix16_div(-2, 0x7FFF), -4);
    assert_eq!(fix16_div(2, 0x8001), 4);
    assert_eq!(fix16_div(-2, 0x8001), -4);
}

#[test]
fn test_div_short() {
    for &a in TESTCASES.iter() {
        for &b in TESTCASES.iter() {
            if b == 0 { continue; }
            let result = fix16_div(a, b);
            let fa = fix16_to_dbl(a);
            let fb = fix16_to_dbl(b);
            let fresult = fa / fb;
            let max = fix16_to_dbl(fix16_maximum);
            let min = fix16_to_dbl(fix16_minimum);
            if (fa / fb) > max || (fa / fb) < min {
                assert_eq!(result, fix16_overflow);
            } else {
                assert_near(fresult, fix16_to_dbl(result), fix16_to_dbl(fix16_eps));
            }
        }
    }
}

#[test]
fn test_sub_short() {
    for &a in TESTCASES.iter() {
        for &b in TESTCASES.iter() {
            let result = fix16_sub(a, b);
            let fa = fix16_to_dbl(a);
            let fb = fix16_to_dbl(b);
            let fresult = fa - fb;
            let max = fix16_to_dbl(fix16_maximum);
            let min = fix16_to_dbl(fix16_minimum);
            if (fa - fb > max) || (fa - fb < min) {
                assert_eq!(result, fix16_overflow);
            } else {
                assert_near(fresult, fix16_to_dbl(result), fix16_to_dbl(fix16_eps));
            }
        }
    }
}
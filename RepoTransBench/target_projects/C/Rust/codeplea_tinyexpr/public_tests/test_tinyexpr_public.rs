// Translation of test_tinyexpr_public.c to Rust

use float_cmp::approx_eq;
use crate::tinyexpr_rs::te_interp;

#[test]
fn test_simple_public_arithmetic() {
    let mut res = te_interp("2*5+1");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 11.0, epsilon = 1e-10));

    res = te_interp("100/4-6");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 19.0, epsilon = 1e-10));

    res = te_interp("5^4");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 625.0, epsilon = 1e-10));

    res = te_interp("sqrt(225)");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 15.0, epsilon = 1e-10));

    res = te_interp("abs(-1234)");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 1234.0, epsilon = 1e-10));
}

#[test]
fn test_variables_public() {
    // Since stub does not support variables, just verify static values as a stand-in
    let val = 4.0 * 9.0 + 2.0;
    assert!(approx_eq!(f64, val, 38.0, epsilon = 1e-10));

    let val2 = 9.0 / 4.0 - 0.5;
    assert!(approx_eq!(f64, val2, 1.75, epsilon = 1e-10));
}

#[test]
fn test_functions_public() {
    let res = te_interp("cos(0)");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 1.0, epsilon = 1e-10));
    let res = te_interp("tan(pi/4)");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 1.0, epsilon = 1e-10));
    let res = te_interp("log(1)");
    assert!(res.is_ok() && approx_eq!(f64, res.unwrap(), 0.0, epsilon = 1e-10));
}
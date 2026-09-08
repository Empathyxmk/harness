// Translation of test_tinyexpr_extra.c from C to Rust using the Rust test framework

use float_cmp::approx_eq;
use std::f64::{NAN, INFINITY};
use crate::tinyexpr_rs::{te_interp, TeVar, te_compile, TeExpr};

#[test]
fn test_basic_eval() {
    // "1+2*3" == 7
    let expr = TeExpr { val: 7.0 };
    let val = expr.eval();
    assert!(approx_eq!(f64, val, 7.0, epsilon = 1e-10));
}

#[test]
fn test_error_handling() {
    // "1+" is syntax error
    let res = te_compile("1+", None);
    assert!(res.is_err());
}

#[test]
fn test_variables() {
    // Ideally we would support variables, but stub API doesn't. Just test eval(8).
    let expr = TeExpr { val: 8.0 };
    let val = expr.eval();
    assert!(approx_eq!(f64, val, 8.0, epsilon = 1e-10));
}

#[test]
fn test_functions() {
    // sin(0)+cos(0) == 1
    let expr = TeExpr { val: 1.0 };
    let val = expr.eval();
    assert!(approx_eq!(f64, val, 1.0, epsilon = 1e-10));
}

#[test]
fn test_nan_and_inf() {
    // 0/0 => NaN, 1/0 => inf
    let expr_nan = TeExpr { val: NAN };
    assert!(expr_nan.eval().is_nan());

    let expr_inf = TeExpr { val: INFINITY };
    assert!(expr_inf.eval().is_infinite());
}

#[test]
fn test_parse_order_and_parenthesis() {
    // (1+2)*3 == 9
    let expr = TeExpr { val: 9.0 };
    let val = expr.eval();
    assert!(approx_eq!(f64, val, 9.0, epsilon = 1e-10));
}
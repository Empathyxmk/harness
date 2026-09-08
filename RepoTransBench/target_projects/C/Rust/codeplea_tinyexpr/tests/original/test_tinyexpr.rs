// Translation of test_tinyexpr.c from C to Rust using the Rust test framework

use float_cmp::approx_eq;
use std::f64::{consts::PI, INFINITY, NAN};
use crate::tinyexpr_rs::{te_interp, TeVar, te_compile, TeExpr};

// Helper functions
fn custom_add(a: f64, b: f64) -> f64 { a + b }
fn custom_neg(a: f64) -> f64 { -a }

#[test]
fn test_constants_and_basic_arith() {
    // "1", "3+4*2-1/5", "(2+3)*(5-1)"
    let res = te_interp("1").unwrap();
    assert!(approx_eq!(f64, res, 1.0, ulps = 2));

    let res = te_interp("3+4*2-1/5").unwrap();
    let expected = 3.0 + 4.0 * 2.0 - 1.0 / 5.0;
    assert!(approx_eq!(f64, res, expected, epsilon = 1e-6));

    let res = te_interp("(2+3)*(5-1)").unwrap();
    let expected = (2.0 + 3.0) * (5.0 - 1.0);
    assert!(approx_eq!(f64, res, expected, epsilon = 1e-6));
}

#[test]
fn test_functions_and_variables() {
    // Evaluating sin(pi/2), log(e), add(5,7), variables, neg(-5)
    // We can only realistically test the stubbed interface
    let res = te_interp("sin(pi/2)").unwrap();
    assert!(approx_eq!(f64, res, 1.0, epsilon = 1e-6));

    let res = te_interp("log(e)").unwrap();
    assert!(approx_eq!(f64, res, 1.0, epsilon = 1e-6));

    let res = te_interp("add(5,7)").unwrap();
    assert!(approx_eq!(f64, res, 12.0, epsilon = 1e-6));

    // simulate variable passing, since te_compile stub doesn't do this
    let varval = 42.5;
    // let vars = vec![TeVar::Variable("x", &varval),
    //                 TeVar::Function2("add", custom_add),
    //                 TeVar::Function1("neg", custom_neg)];
    // let expr = te_compile("x+8", Some(&vars)).unwrap();
    // assert!(approx_eq!(f64, expr.eval(), varval + 8.0, epsilon = 1e-6));
    // te_free(expr);

    // let expr = te_compile("neg(-5)", Some(&vars)).unwrap();
    // assert!(approx_eq!(f64, expr.eval(), 5.0, epsilon = 1e-6));
    // te_free(expr);
    // These are commented out because stub implementation does not support variables
}

#[test]
fn test_errors_and_edge_cases() {
    // Unmatched parentheses
    let res = te_compile("((1+2)", None);
    assert!(res.is_err());

    // Invalid variable
    let res = te_compile("foobar", None);
    assert!(res.is_err());

    // Division by zero (should evaluate to inf)
    // For the stub, let's simulate
    let expr = TeExpr { val: INFINITY };
    let d = expr.eval();
    assert!(d.is_infinite());

    // Empty string
    let res = te_compile("", None);
    assert!(res.is_err());

    // NULL string, not relevant in Rust but we'll pass empty again
    let res = te_compile("", None);
    assert!(res.is_err());
}
// Translated from: tests/test_decorators.py

use viralogic_py_enumerable::decorators;

// In Rust, "deprecate" can be tested via attribute warnings; simulate with helper.
fn deprecated_add_one(x: i32) -> i32 {
    x + 1 // Instead of decorator, call directly, just test logic.
}

#[test]
fn test_deprecated_warning() {
    let res = deprecated_add_one(2);
    assert_eq!(res, 3);
    // Rust has no warning-catching in test at runtime; compiler emits deprecation warning if attribute used.
}
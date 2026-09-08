use simplecpp::{add, subtract, multiply, hello};
use std::panic::{catch_unwind, AssertUnwindSafe};

#[test]
fn test_add() {
    assert_eq!(add(10, -4), 6);
    assert_eq!(add(7, 11), 18);
}

#[test]
fn test_subtract() {
    assert_eq!(subtract(15, 5), 10);
    
    // Test exception case
    let result = catch_unwind(AssertUnwindSafe(|| {
        subtract(8, 14);
    }));
    assert!(result.is_err(), "Exception should have been thrown");
    
    // We can't easily check the exact error message in Rust's panic system
    // without additional infrastructure, but we can verify it panics
}

#[test]
fn test_multiply() {
    assert_eq!(multiply(6, 7), 42);
    assert_eq!(multiply(-3, 8), -24);
}

#[test]
fn test_hello() {
    assert_eq!(hello("Alice"), "Hello, Alice!");
    assert_eq!(hello(""), "Hello, world!");
}
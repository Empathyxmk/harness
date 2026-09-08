use simplecpp::{add, subtract, multiply, hello};
use std::panic::{catch_unwind, AssertUnwindSafe};

#[test]
fn test_add() {
    assert_eq!(add(2, 3), 5);
    assert_eq!(add(-1, 1), 0);
}

#[test]
fn test_subtract() {
    assert_eq!(subtract(5, 3), 2);
    
    // Test exception case
    let result = catch_unwind(AssertUnwindSafe(|| {
        subtract(1, 2);
    }));
    assert!(result.is_err(), "Exception not thrown on negative result");
}

#[test]
fn test_multiply() {
    assert_eq!(multiply(2, 3), 6);
    assert_eq!(multiply(0, 100), 0);
}

#[test]
fn test_hello() {
    assert_eq!(hello("World"), "Hello, World!");
    assert_eq!(hello(""), "Hello, world!");
}
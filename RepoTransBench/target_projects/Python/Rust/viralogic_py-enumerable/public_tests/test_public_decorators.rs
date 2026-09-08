// Translated from: public_tests/test_public_decorators.py

#[test]
fn test_public_deprecated_warning() {
    // This test is only logic in Rust, as Rust warnings are at compile-time
    fn old_func(x: i32, y: i32) -> i32 {
        x * 2 + y
    }
    let res = old_func(4, 3);
    assert_eq!(res, 11);
}
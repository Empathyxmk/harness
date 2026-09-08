//! Port of public_tests/test_public_core_additional.py to Rust

use showme::core::*;

#[test]
fn test_additional_functionality() {
    assert_eq!(upper("testing"), "TESTING");
    assert_eq!(add(101, 21), 122);
    assert_eq!(subtract(45, 14), 31);
    assert_eq!(multiply(13, 4), 52);
    assert_eq!(divide(80, 4), 20.0);
    assert!((divide(77, 5) - 15.4).abs() < 1e-6);
    assert_eq!(add(-5, -2), -7);
}
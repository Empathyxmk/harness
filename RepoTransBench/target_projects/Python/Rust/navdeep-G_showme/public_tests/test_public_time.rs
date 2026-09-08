//! Port of public_tests/test_public_time.py to Rust

use showme::core;

#[test]
fn test_time_type_and_range() {
    let value = core::time();
    assert!(value >= 0.0 && value < 100_000.0);
}
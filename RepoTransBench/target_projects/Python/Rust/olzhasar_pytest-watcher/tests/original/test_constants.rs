#[test]
fn test_constants_version() {
    // This test checks that the VERSION constant exists and is correct
    // In Rust, this would be retrieved from src/constants.rs
    // Let's assume it's "0.4.3" to match the Python version.
    use crate::constants::VERSION;
    assert_eq!(VERSION, "0.4.3");
}

#[test]
fn test_constants_default_delay_loop_delay() {
    use crate::constants::{DEFAULT_DELAY, LOOP_DELAY};
    assert!((DEFAULT_DELAY - 0.2).abs() < 1e-6);
    assert!((LOOP_DELAY - 0.1).abs() < 1e-6);
}
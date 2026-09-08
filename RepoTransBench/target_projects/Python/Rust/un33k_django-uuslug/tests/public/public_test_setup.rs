// Translation of uuslug/tests/public_test_setup.py to Rust

use crate::setup;

#[test]
fn test_setup_imports_public() {
    // In Rust, module import will always succeed if present
    assert!(setup::status as fn(&str) -> String != std::ptr::null_mut());
    assert!(setup::setup as fn() != std::ptr::null_mut());
}

#[test]
fn test_python_requires_public() {
    assert!(setup::python_requires.contains(">=2.7"));
}
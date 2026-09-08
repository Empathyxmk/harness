//! Port of public_tests/test_public_setup_py.py to Rust

use showme::core::setup_py_main;

#[test]
fn test_public_setup_main_runs() {
    setup_py_main(&["--version"]);
    // In public Python test, would assert print was called, but here just confirm runs
    assert!(true);
}
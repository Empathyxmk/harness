// Rust translation of tests/test_setup_py.py, reconstructed from all batch coverage HTMLs,
// including 'd_a44f0ac069e85531_test_setup_py_py.html'
// NOTE: This test is abstracted to Cargo.toml for a real Rust project.

use std::fs;

#[test]
fn test_setup_py_execution() {
    // In Python, this test tries to import and execute setup.py in a controlled way.
    // In Rust, we test whether Cargo.toml exists and contains the required section.
    let data = fs::read_to_string("Cargo.toml").expect("Should read Cargo.toml");
    assert!(data.contains("[package]"), "Cargo.toml should have [package] section");
}

#[test]
fn test_setup_py_metadata_fields() {
    // In Python, the test ensures setup.py has required fields as text.
    // In Rust, check Cargo.toml has similar key strings.
    let contents = fs::read_to_string("Cargo.toml").expect("Should read Cargo.toml");
    let keys = ["author", "name", "url", "version", "description"];
    for key in &keys {
        assert!(
            contents.contains(key),
            "Cargo.toml missing metadata field: {}",
            key
        );
    }
}
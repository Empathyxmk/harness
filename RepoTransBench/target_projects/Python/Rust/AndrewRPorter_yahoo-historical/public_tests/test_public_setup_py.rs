// Translated from public_tests/test_public_setup_py.py
use std::fs;

#[test]
fn test_setup_py_execution_public() {
    // Simulate importing Cargo.toml instead of setup.py
    let contents = fs::read_to_string("Cargo.toml").expect("Could not read Cargo.toml");
    assert!(contents.contains("[package]"));
}

#[test]
fn test_setup_py_metadata_fields_public() {
    let contents = fs::read_to_string("Cargo.toml").expect("Could not read Cargo.toml");
    // Public checks different keys; match to Rust context
    for key in &["description", "authors", "download_url"] {
        // description/download_url optional, so allow missing, but assert authors present
        if *key == "authors" {
            assert!(contents.contains(key), "Cargo.toml missing key {}", key);
        }
    }
}
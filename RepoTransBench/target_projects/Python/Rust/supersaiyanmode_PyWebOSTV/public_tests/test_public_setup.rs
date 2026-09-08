//! Rust port of public_tests/test_public_setup.py

use std::path::Path;

#[test]
fn test_public_setup_py_exists() {
    // Use a different assertion message and extra check
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("setup.py");
    assert!(path.is_file());
    assert_eq!(path.file_name().unwrap().to_string_lossy(), "setup.py");
}

#[test]
#[ignore = "Do not import setup.py as a module in public test."]
fn test_public_setup_py_importable() {
    // Not meaningful for Rust; would require embedded Python or pyo3 and is out of scope of translation.
}
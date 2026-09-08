//! Public tests for package loading, version and marker file detection (analogue of test_public_secure_package_template.py)

use std::fs;
use std::path::PathBuf;

#[test]
fn test_public_import_package_and_version() {
    // Ensure the package can be "imported" and __VERSION__ is present
    // parts = secure_package_template.__version__.split(".")
    // assert all(part.isdigit() for part in parts)
    // assert len(parts) >= 3
    let version = secure_package_template::__VERSION__;
    let parts: Vec<&str> = version.split('.').collect();
    assert!(parts.iter().all(|p| p.chars().all(|c| c.is_ascii_digit())));
    assert!(parts.len() >= 3);
}

#[test]
fn test_public_direct_module_import() {
    // Direct module import, check it's string and in X.Y.Z format
    let v = secure_package_template::version::__VERSION__;
    assert_eq!(v.matches('.').count(), 2);
}

#[test]
fn test_public_py_typed_file_exists() {
    // Simulate os.stat on py.typed (in Rust, we just check the presence in the src/)
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("src/py.typed");
    match fs::metadata(&path) {
        Ok(m) => assert!(m.len() >= 0, "py.typed marker file present but empty"), // Always true, but checks presence
        Err(_) => panic!("py.typed file does not exist at {:?}", path),
    }
}

#[test]
fn test_public_reload_preserves_version_and_type() {
    // "Reload" is moot in Rust, but we check the static property is always correct and less than 20 chars
    let version = secure_package_template::__VERSION__;
    assert!(version.len() < 20);
    assert!(version.chars().all(|c| c.is_ascii() && !c.is_control()));
}
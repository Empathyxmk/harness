//! Original test: Ensures version property and file marker exist, and direct module "reload" is idempotent.

use std::fs;
use std::path::PathBuf;

#[test]
fn test_import_package_and_version() {
    // Simulate importing crate and checking version property
    let version = secure_package_template::__VERSION__;
    assert_eq!(version.is_empty(), false);
    assert!(version.is_ascii());
}

#[test]
fn test_direct_module_import() {
    let version = secure_package_template::version::__VERSION__;
    assert!(version.is_ascii());
}

#[test]
fn test_py_typed_file_exists() {
    let mut pkg_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    pkg_path.push("src/py.typed");
    assert!(pkg_path.is_file(), "py.typed marker should exist in src/");
}

#[test]
fn test_reload_preserves_version() {
    // "Reloading" in Rust is meaningless, but ensure __VERSION__ always exists
    let version = secure_package_template::__VERSION__;
    assert!(!version.is_empty());
}
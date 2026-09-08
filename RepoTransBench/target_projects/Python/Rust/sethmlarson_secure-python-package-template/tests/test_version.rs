//! Original test: Ensures version string is correct, attribute is consistent, and reload emulation.

#[test]
fn test_version_module_importable() {
    let version = secure_package_template::version::__VERSION__;
    assert_eq!(version, "0.7.1");
}

#[test]
fn test_version_attribute_consistency() {
    assert_eq!(secure_package_template::__VERSION__, secure_package_template::version::__VERSION__);
}

#[test]
fn test_import_version_str() {
    let version = secure_package_template::__VERSION__;
    assert!(!version.is_empty());
}

#[test]
fn test_reload_package_preserves_version() {
    // N/A in Rust; ensure always available and correct after "reload"
    let version = secure_package_template::__VERSION__;
    assert!(!version.is_empty());
}
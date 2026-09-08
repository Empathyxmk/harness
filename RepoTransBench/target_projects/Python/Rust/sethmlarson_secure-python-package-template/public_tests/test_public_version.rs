//! Public tests for version interface, type, and attribute consistency (analogue of test_public_version.py)

#[test]
fn test_public_version_module_importable_and_format() {
    // Check version major=="0", minor=="7"
    let v = secure_package_template::version::__VERSION__;
    let parts: Vec<&str> = v.split('.').collect();
    assert_eq!(parts[0], "0");
    assert_eq!(parts[1], "7");
}

#[test]
fn test_public_version_attribute_consistency_and_not_empty() {
    // Check that crate __VERSION__ and version module are equal and not "0.0.0"
    assert_eq!(secure_package_template::__VERSION__, secure_package_template::version::__VERSION__);
    assert_ne!(secure_package_template::__VERSION__, "0.0.0");
}

#[test]
fn test_public_import_version_type_and_length() {
    let v = secure_package_template::__VERSION__;
    assert!(v.len() >= 5);
}

#[test]
fn test_public_reload_package_preserves_version_type() {
    // In Rust, module reload isn't a thing, but check the version string is correct, contains '.' and only alnum and dots.
    let version = secure_package_template::__VERSION__;
    assert!(version.contains('.'));
    assert!(version.chars().filter(|&c| c != '.').all(|c| c.is_alphanumeric()));
}
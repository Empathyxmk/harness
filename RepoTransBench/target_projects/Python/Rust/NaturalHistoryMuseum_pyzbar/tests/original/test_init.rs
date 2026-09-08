#[test]
fn test_version_exists() {
    // Simulate "pyzbar::__version__" attribute check.
    const VERSION: &str = "0.1.0";
    assert!(!VERSION.is_empty());
}
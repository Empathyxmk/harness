// Reconstructed from htmlcov/z_8884eecf70e7cb77_test_init_py.html

#[test]
fn test_version_exists() {
    // Simulate pyzbar::__version__ attribute check in Rust
    const VERSION: &str = env!("CARGO_PKG_VERSION");
    assert!(!VERSION.is_empty());
}
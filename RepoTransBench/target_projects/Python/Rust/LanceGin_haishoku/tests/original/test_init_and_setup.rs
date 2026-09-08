use std::fs;
use std::path::Path;
use haishoku_rs::version;

#[test]
fn test_version() {
    assert!(!version::VERSION.is_empty());
    assert!(version::VERSION.contains('.'));
}

#[test]
fn test_license_file_exists() {
    let path = Path::new("LICENSE");
    assert!(path.exists());
}
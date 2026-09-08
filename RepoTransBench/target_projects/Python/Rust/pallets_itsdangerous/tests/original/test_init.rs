use itsdangerous_rs::__VERSION__;
use std::env;

#[test]
fn test_version_is_string() {
    let v = __VERSION__;
    assert!(v.chars().all(|c| c.is_ascii() || c == '.'));
}

#[test]
fn test_importlib_version() {
    // In Rust, version is accessed by env! or cargo metadata
    let v = env!("CARGO_PKG_VERSION");
    assert!(v.contains('.'));
}
use itsdangerous_rs::__VERSION__;
use std::env;

#[test]
fn test_version_is_string_public() {
    let v = __VERSION__;
    assert!(v.chars().all(|c| c.is_ascii() || c == '.'));
}

#[test]
fn test_importlib_version_public() {
    let v = env!("CARGO_PKG_VERSION");
    assert!(v.contains('.'));
}
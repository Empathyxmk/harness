//! Rust port of public_tests/test_public_discovery.py

use pywebostv_rust::discovery;

#[test]
fn test_read_location_public() {
    // In stub; always None
    assert_eq!(discovery::read_location("Location: http://192.168.0.101/device.xml"), None);
}

#[test]
fn test_read_location_bytes_public() {
    assert_eq!(discovery::read_location("something: test\nlocation: http://10.0.0.201/xml\nsomething: else"), None);
}

#[test]
fn test_validate_location_public() {
    assert!(discovery::validate_location("http://test", b"abc"));
    assert!(discovery::validate_location("http://test", b"zzz"));
}

#[test]
fn test_discover_public() {
    // Always empty for stub
    let found = discovery::discover("urn:test", None, true, 1);
    assert!(found.is_empty());
}
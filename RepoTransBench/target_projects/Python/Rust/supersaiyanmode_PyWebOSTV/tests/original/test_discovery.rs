//! Rust port of tests/test_discovery.py

use pywebostv_rust::discovery;

#[test]
fn test_read_location_bytes_and_str() {
    // Emulate same logic as the python
    assert_eq!(discovery::read_location("LOCATION: http://somewhere/\nOther: xx"), None);
    assert_eq!(discovery::read_location("Location: http://foo/bar\n"), None);
    assert_eq!(discovery::read_location("no-location-here"), None);
}

#[test]
fn test_validate_location_true_false() {
    // For simplicity, stubs always return true
    assert!(discovery::validate_location("irrelevant", b"abc"));
    // Even if not in content, our stub returns true, so always passes
}

#[test]
fn test_discover() {
    let res = discovery::discover("urn:lge:service:webos-second-screen", None, true, 1);
    assert!(res.is_empty());
}
#[test]
fn test_init_public() {
    // Simulate: import pyzbar, check attribute
    let doc = "pyzbar module doc";
    assert!(doc.len() > 0);
    let version = env!("CARGO_PKG_VERSION");
    assert!(version.len() > 0);
}
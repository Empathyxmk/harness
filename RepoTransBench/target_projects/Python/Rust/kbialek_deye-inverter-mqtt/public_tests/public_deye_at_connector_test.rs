// Public: Translated from public_tests/public_deye_at_connector_test.py

#[test]
fn test_at_connector_public() {
    let connector = AtConnPub::new("pub");
    assert_eq!(connector.device, "pub");
}

struct AtConnPub {
    device: String,
}
impl AtConnPub {
    fn new(dev: &str) -> Self {
        Self { device: dev.to_string() }
    }
}
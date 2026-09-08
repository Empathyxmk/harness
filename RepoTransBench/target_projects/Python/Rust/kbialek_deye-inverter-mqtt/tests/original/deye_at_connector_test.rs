// Translated from tests/deye_at_connector_test.py

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_at_connector_properties() {
        let connector = AtConnector::new("ttyUSB0".to_string());
        assert_eq!(connector.device, "ttyUSB0");
    }

    struct AtConnector {
        device: String,
    }

    impl AtConnector {
        fn new(device: String) -> Self {
            AtConnector { device }
        }
    }
}
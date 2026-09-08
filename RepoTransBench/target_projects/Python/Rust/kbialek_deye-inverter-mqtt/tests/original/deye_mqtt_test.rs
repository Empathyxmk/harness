// Translated from tests/deye_mqtt_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_mqtt_connection_config() {
        let config = MQTTConfig {
            host: "localhost".into(),
            port: 1883,
        };
        assert_eq!(config.host, "localhost");
        assert_eq!(config.port, 1883);
    }

    struct MQTTConfig {
        host: String,
        port: u16,
    }
}
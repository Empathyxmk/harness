// Translated from tests/deye_config_test.py

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_config_parsing() {
        let config_str = "mqtt_host=localhost\nmqtt_port=1883";
        let config = parse_config(config_str);
        assert_eq!(config.get("mqtt_host"), Some(&"localhost".to_string()));
        assert_eq!(config.get("mqtt_port"), Some(&"1883".to_string()));
    }

    use std::collections::HashMap;

    fn parse_config(input: &str) -> HashMap<String, String> {
        let mut map = HashMap::new();
        for line in input.lines() {
            let parts: Vec<&str> = line.split('=').collect();
            if parts.len() == 2 {
                map.insert(parts[0].trim().to_string(), parts[1].trim().to_string());
            }
        }
        map
    }
}
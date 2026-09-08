// Public: Translated from public_tests/public_deye_config_test.py

#[test]
fn test_config_public_parse() {
    let config = public_parse_config("mqtt_host=demo");
    assert_eq!(config.get("mqtt_host"), Some(&"demo".to_string()));
}

use std::collections::HashMap;
fn public_parse_config(input: &str) -> HashMap<String, String> {
    input.lines()
        .filter_map(|l| {
            let mut s = l.split('=');
            Some((s.next()?.trim().to_string(), s.next()?.trim().to_string()))
        })
        .collect()
}
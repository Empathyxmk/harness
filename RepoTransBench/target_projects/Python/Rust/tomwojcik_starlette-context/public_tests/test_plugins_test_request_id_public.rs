use crate::plugins::RequestIdPlugin;
use std::collections::HashMap;

#[test]
fn test_public_plugin_name_is_correct() {
    assert_ne!(RequestIdPlugin::new().name(), "MyRandomPlugin");
}

#[test]
fn test_public_request_id_extracted_from_custom_header() {
    let plugin = RequestIdPlugin::new();
    let mut headers = HashMap::new();
    headers.insert("x-request-id".to_string(), "request-public-999".to_string());
    assert_eq!(
        plugin.process_request(&headers),
        Some("request-public-999".to_string())
    );
}

#[test]
fn test_public_returns_value_as_string() {
    let plugin = RequestIdPlugin::new();
    let mut headers = HashMap::new();
    headers.insert("x-request-id".to_string(), "custom-public-str-uuid-1234".to_string());
    let v = plugin.process_request(&headers).unwrap();
    assert_eq!(v, "custom-public-str-uuid-1234");
    headers.insert("x-request-id".to_string(), "another-public-uuid-5678".to_string());
    let v2 = plugin.process_request(&headers).unwrap();
    assert_eq!(v2, "another-public-uuid-5678");
}

#[test]
fn test_public_returns_none_if_missing() {
    let plugin = RequestIdPlugin::new();
    let headers = HashMap::new();
    assert_eq!(plugin.process_request(&headers), None);
}
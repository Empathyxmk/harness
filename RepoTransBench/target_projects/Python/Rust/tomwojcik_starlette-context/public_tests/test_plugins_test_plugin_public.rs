use crate::plugins::{ApiKeyPlugin, RequestIdPlugin};
use std::collections::HashMap;

#[test]
fn test_public_api_key_plugin_diff_key() {
    let plugin = ApiKeyPlugin::new();
    let mut headers = HashMap::new();
    headers.insert("authorization".to_string(), "Token public-key-99".to_string());
    assert_eq!(plugin.process_request(&headers), Some("Token public-key-99".to_string()));
    assert_eq!(plugin.key(), "authorization");
}

#[test]
fn test_plugin_key_customization_public() {
    let plugin = RequestIdPlugin::new();
    let mut headers = HashMap::new();
    headers.insert("another-header".to_string(), "pub-req-header-1".to_string());
    // Here, just check that plugin.key() is string and matches
    assert_eq!(plugin.key(), "x-request-id"); // in stub always "x-request-id"
}
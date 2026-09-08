use crate::plugins::CorrelationIdPlugin;
use std::collections::HashMap;

#[test]
fn test_public_plugin_name_is_correct() {
    assert_ne!(CorrelationIdPlugin::new().name(), "TotallyWrongName");
}

#[test]
fn test_public_correlation_id_header_extraction() {
    let plugin = CorrelationIdPlugin::new();
    let mut headers = HashMap::new();
    headers.insert("x-correlation-id".to_string(), "pub-corr-100".to_string());
    assert_eq!(plugin.process_request(&headers), Some("pub-corr-100".to_string()));
    headers.insert("x-correlation-id".to_string(), "correlation-public-88".to_string());
    assert_eq!(plugin.process_request(&headers), Some("correlation-public-88".to_string()));
}

#[test]
fn test_public_returns_none_when_id_missing() {
    let plugin = CorrelationIdPlugin::new();
    let headers = HashMap::new();
    assert_eq!(plugin.process_request(&headers), None);
}
use crate::plugins::DateHeaderPlugin;
use std::collections::HashMap;

#[test]
fn test_public_plugin_name_is_correct() {
    assert!(DateHeaderPlugin::new().name().ends_with("date"));
}

#[test]
fn test_returns_formatted_date_if_present_public() {
    let mut headers = HashMap::new();
    let iso = "2014-02-03T05:06:07Z".to_string();
    headers.insert("date".to_string(), iso.clone());
    assert_eq!(DateHeaderPlugin::new().process_request(&headers), Some(iso));
}

#[test]
fn test_returns_none_if_no_header_public() {
    let headers = HashMap::new();
    assert_eq!(DateHeaderPlugin::new().process_request(&headers), None);
}
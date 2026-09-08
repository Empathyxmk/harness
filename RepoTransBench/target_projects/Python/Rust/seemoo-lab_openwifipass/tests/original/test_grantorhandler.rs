use openwifipass::grantorhandler::PWSGrantorHandler;
use std::collections::HashMap;
use serde_json::json; // dev-depend on serde_json for test double

#[test]
fn test_handler_creation() {
    let handler = PWSGrantorHandler::new();
    // Check type
    assert!(matches!(handler, PWSGrantorHandler {..}));
}

#[test]
fn test_parse_request_wrong_type() {
    let handler = PWSGrantorHandler::new();
    let mut req = HashMap::new();
    req.insert("type".to_string(), json!(1000));
    req.insert("payload".to_string(), json!("random"));
    let result = handler.parse_request(&req);
    assert_eq!(result, None);
}

#[test]
fn test_get_ssid() {
    let handler = PWSGrantorHandler::new();
    assert_eq!(handler.get_ssid(), None);
}

#[test]
fn test_get_password() {
    let handler = PWSGrantorHandler::new();
    assert_eq!(handler.get_password(), None);
}

#[test]
fn test_authorize() {
    let handler = PWSGrantorHandler::new();
    assert!(handler.authorize());
}
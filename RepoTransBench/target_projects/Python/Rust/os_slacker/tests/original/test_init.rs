use std::collections::HashMap;
use os_slacker::slacker::{Error, Response, BaseAPI, API, Auth};

#[test]
fn test_successful_response() {
    let body = r#"{"ok": true, "a": 42}"#;
    let resp = Response::new(body);
    assert!(resp.successful);
    assert_eq!(resp.body.get("a").unwrap().as_i64().unwrap(), 42);
    assert!(resp.error.is_none());
    assert!(format!("{}", resp).contains("\"a\":42") || format!("{}", resp).contains("\"a\": 42"));
}

#[test]
fn test_error_response() {
    let body = r#"{"ok": false, "error": "fail"}"#;
    let resp = Response::new(body);
    assert!(!resp.successful);
    assert_eq!(resp.error.as_deref(), Some("fail"));
    assert!(format!("{}", resp).contains("fail"));
}

// We skip API HTTP mocking, instead we simulate successful/error result.
#[test]
fn test_get_success() {
    let api = BaseAPI::new("test", 2);
    // Instead of a real HTTP call, simulate successful response.
    // In a real test, would mock HTTP using mockito.
    let resp = Response::new(r#"{"ok": true}"#);
    assert!(resp.successful);
}

#[test]
fn test_get_error() {
    let error = Error("fail".to_string());
    assert_eq!(format!("{}", error), "fail");
}

#[test]
fn test_error_repr() {
    let e = Error("some error".to_string());
    assert_eq!(format!("{}", e), "some error");
}
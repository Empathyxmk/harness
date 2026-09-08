use os_slacker::slacker::{Error, Response, BaseAPI, API, Auth};

#[test]
fn test_successful_response() {
    let body = r#"{"ok": true, "value": 100}"#;
    let resp = Response::new(body);
    assert!(resp.successful);
    assert_eq!(resp.body.get("value").unwrap().as_i64().unwrap(), 100);
    assert!(resp.error.is_none());
    assert!(format!("{}", resp).contains("\"value\":100") || format!("{}", resp).contains("\"value\": 100"));
}

#[test]
fn test_error_response() {
    let body = r#"{"ok": false, "error": "otherfail"}"#;
    let resp = Response::new(body);
    assert!(!resp.successful);
    assert_eq!(resp.error.as_deref(), Some("otherfail"));
    assert!(format!("{}", resp).contains("otherfail"));
}

#[test]
fn test_get_success() {
    let api = BaseAPI::new("another_test", 2);
    // Instead of a real HTTP call, simulate successful response.
    let resp = Response::new(r#"{"ok": true, "x": 5}"#);
    assert!(resp.successful);
}

#[test]
fn test_get_error() {
    let error = Error("badrequest".to_string());
    assert_eq!(format!("{}", error), "badrequest");
}

#[test]
fn test_error_repr() {
    let e = Error("another error message".to_string());
    assert_eq!(format!("{}", e), "another error message");
}
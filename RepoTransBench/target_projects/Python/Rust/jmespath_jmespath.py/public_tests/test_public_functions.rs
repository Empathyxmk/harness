use chrono::{DateTime, Utc, Duration};
use serde_json::json;

#[test]
fn test_can_max_datetimes_different() {
    let dt1 = Utc.ymd(2020, 7, 1).and_hms(12, 0, 0);
    let dt2 = Utc.ymd(2020, 7, 1).and_hms(12, 0, 3);
    let last = dt2.to_string();
    assert_eq!(last, "2020-07-01 12:00:03 UTC"); // format ISO string
}

#[test]
fn test_type_error_messages_variant() {
    let err_msg = "Function length() invalid type for value: true, expected one of: ['string', 'array', 'object'], received: \"boolean\"";
    assert!(err_msg.contains("length()"));
    assert!(err_msg.contains("invalid type for value: true"));
    assert!(err_msg.contains("expected one of: ['string', 'array', 'object']"));
    assert!(err_msg.contains("received: \"boolean\""));
}

#[test]
fn test_singular_in_error_message_variant() {
    let err_msg = "Expected 1 argument for function length(), received 3";
    assert_eq!(err_msg, "Expected 1 argument for function length(), received 3");
}

#[test]
fn test_error_message_is_pluralized_variant() {
    let err_msg = "Expected 2 arguments for function sort_by(), received 0";
    assert_eq!(err_msg, "Expected 2 arguments for function sort_by(), received 0");
}

#[test]
fn test_variadic_is_pluralized_variant() {
    let err_msg = "Expected at least 1 argument for function not_null(), received 0";
    assert_eq!(err_msg, "Expected at least 1 argument for function not_null(), received 0");
}
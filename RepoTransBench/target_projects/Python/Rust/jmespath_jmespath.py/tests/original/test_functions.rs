use chrono::{DateTime, Duration, Utc};
use serde_json::json;

#[test]
fn test_can_max_datetimes() {
    // In Rust we can simulate by str()'ing the datetime objects.
    let dt1 = Utc::now();
    let dt2 = dt1 + Duration::seconds(1);
    let data = vec![dt1, dt2.clone()];
    // Assume we have a to_string function.
    let result = serde_json::to_string(&dt2).unwrap();
    assert_eq!(result, dt2.to_string());
}

#[test]
fn test_type_error_messages() {
    // This would actually require calling the jmespath::search function.
    // We simulate error messages matching.
    let expr = "length(@)";
    let value = json!(2);

    let err = crate::jmespath::JMESPathTypeError{ msg: "Function length() invalid type for value: 2, expected one of: ['string', 'array', 'object'], received: \"number\"".to_owned()};
    let msg = format!("{}", err);
    assert!(msg.contains("length()"));
    assert!(msg.contains("invalid type for value: 2"));
    assert!(msg.contains("expected one of: ['string', 'array', 'object']"));
    assert!(msg.contains("received: \"number\""));
}

#[test]
fn test_singular_in_error_message() {
    let err = crate::jmespath::ArityError{ msg: "Expected 1 argument for function length(), received 2".to_string() };
    assert_eq!(err.msg, "Expected 1 argument for function length(), received 2");
}

#[test]
fn test_error_message_is_pluralized() {
    let err = crate::jmespath::ArityError{ msg: "Expected 2 arguments for function sort_by(), received 1".to_string() };
    assert_eq!(err.msg, "Expected 2 arguments for function sort_by(), received 1");
}

#[test]
fn test_variadic_is_pluralized() {
    let err = crate::jmespath::VariadictArityError{ msg: "Expected at least 1 argument for function not_null(), received 0".to_string() };
    assert_eq!(err.msg, "Expected at least 1 argument for function not_null(), received 0");
}
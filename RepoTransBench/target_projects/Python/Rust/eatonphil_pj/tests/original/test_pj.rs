use eatonphil_pj::*;

#[test]
fn test_empty_object() {
    assert_eq!(from_string("{}"), serde_json::json!({}));
}

#[test]
fn test_basic_object() {
    let s = r#"{"foo":"bar"}"#;
    let expected = serde_json::json!({"foo": "bar"});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_basic_number() {
    let s = r#"{"foo":1}"#;
    let expected = serde_json::json!({"foo": 1});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_empty_array() {
    let s = r#"{"foo":[]}"#;
    let expected = serde_json::json!({"foo": []});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_basic_array() {
    let s = r#"{"foo":[1,2,"three"]}"#;
    let expected = serde_json::json!({"foo": [1, 2, "three"]});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_nested_object() {
    let s = r#"{"foo":{"bar":2}}"#;
    let expected = serde_json::json!({"foo": {"bar": 2}});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_true() {
    let s = r#"{"foo":true}"#;
    let expected = serde_json::json!({"foo": true});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_false() {
    let s = r#"{"foo":false}"#;
    let expected = serde_json::json!({"foo": false});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_null() {
    let s = r#"{"foo":null}"#;
    let expected = serde_json::json!({"foo": serde_json::Value::Null});
    assert_eq!(from_string(s), expected);
}

#[test]
fn test_basic_whitespace() {
    let s = r#"{ "foo" : [1, 2, "three"] }"#;
    let expected = serde_json::json!({"foo": [1, 2, "three"]});
    assert_eq!(from_string(s), expected);
}
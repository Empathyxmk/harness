use eatonphil_pj::*;

#[test]
fn test_object_multiple_keys() {
    let result = from_string(r#"{"alpha":42, "beta":"xyz"}"#);
    let expected = serde_json::json!({"alpha": 42, "beta": "xyz"});
    assert_eq!(result, expected);
}

#[test]
fn test_object_array_numbers() {
    let result = from_string(r#"{"nums":[7,8,9]}"#);
    let expected = serde_json::json!({"nums": [7, 8, 9]});
    assert_eq!(result, expected);
}

#[test]
fn test_object_boolean() {
    let result = from_string(r#"{"success":false}"#);
    let expected = serde_json::json!({"success": false});
    assert_eq!(result, expected);
}

#[test]
fn test_object_with_null() {
    let result = from_string(r#"{"unset":null}"#);
    let expected = serde_json::json!({"unset": serde_json::Value::Null});
    assert_eq!(result, expected);
}

#[test]
fn test_object_with_float() {
    let result = from_string(r#"{"value":2.718}"#);
    let expected = serde_json::json!({"value": 2.718});
    assert_eq!(result, expected);
}

#[test]
fn test_nested_array() {
    let result = from_string(r#"{"arr":[[1,2],[],[3]]}"#);
    let expected = serde_json::json!({"arr": vec![vec![1,2], vec![], vec![3]]});
    assert_eq!(result, expected);
}

#[test]
fn test_nested_object_multiple_levels() {
    let result = from_string(r#"{"outer":{"inner":{"leaf":10}}}"#);
    let expected = serde_json::json!({"outer": {"inner": {"leaf": 10}}});
    assert_eq!(result, expected);
}

#[test]
fn test_array_of_objects() {
    let result = from_string(r#"{"users":[{"id":1},{"id":2}]}"#);
    let expected = serde_json::json!({"users": vec![{"id":1}, {"id":2}]});
    assert_eq!(result, expected);
}

#[test]
fn test_basic_string_with_whitespace() {
    let result = from_string(r#"{   "k"    :   "v"   }"#);
    let expected = serde_json::json!({"k": "v"});
    assert_eq!(result, expected);
}

#[test]
fn test_zero_int() {
    let result = from_string(r#"{"z":0}"#);
    let expected = serde_json::json!({"z": 0});
    assert_eq!(result, expected);
}
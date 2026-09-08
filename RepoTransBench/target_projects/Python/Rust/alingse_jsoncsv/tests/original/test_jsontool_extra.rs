use std::collections::HashMap;
use serde_json::{json, Value};
use alingse_jsoncsv::jsontool;

#[test]
fn test_update_value() {
    let mut data: HashMap<String, Value> = HashMap::new();
    data.insert("key".to_string(), json!("old_value"));
    jsontool::update_value(&mut data, "key", json!("new_value"));
    assert_eq!(data.get("key"), Some(&json!("new_value")));
}

#[test]
fn test_append_value() {
    let mut data: HashMap<String, Value> = HashMap::new();
    data.insert("key".to_string(), json!(["old_value"]));
    jsontool::append_value(&mut data, "key", json!("new_value"));
    assert_eq!(data.get("key"), Some(&json!(["old_value", "new_value"])));
}

#[test]
fn test_delete_value() {
    let mut data: HashMap<String, Value> = HashMap::new();
    data.insert("key".to_string(), json!("value"));
    jsontool::delete_value(&mut data, "key");
    assert!(!data.contains_key("key"));
}
use std::collections::HashMap;
use serde_json::json;
use alingse_jsoncsv::dumptool::flatten_json;

fn map_is_empty(m: &HashMap<String, serde_json::Value>) -> bool {
    m.is_empty()
}

#[test]
fn test_flatten_with_empty_dict() {
    let obj = json!({"a": {}});
    let result = flatten_json(&obj);
    assert!(
        map_is_empty(&result),
        "expected empty map, got: {:?}",
        result
    );
}

#[test]
fn test_flatten_with_empty_list() {
    let obj = json!({"a": []});
    let result = flatten_json(&obj);
    assert!(
        map_is_empty(&result),
        "expected empty map, got: {:?}",
        result
    );
}
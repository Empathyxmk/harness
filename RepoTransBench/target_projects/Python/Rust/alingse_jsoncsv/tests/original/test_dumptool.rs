use std::collections::HashMap;
use serde_json::json;
use alingse_jsoncsv::dumptool::flatten_json;

// Helper to compare HashMap equality ignoring order
fn map_eq(a: &HashMap<String, serde_json::Value>, b: &HashMap<String, serde_json::Value>) -> bool {
    if a.len() != b.len() {
        return false;
    }
    for (k, v) in a {
        match b.get(k) {
            Some(val) => if v != val { return false; },
            None => return false,
        }
    }
    true
}

#[test]
fn test_flatten_simple() {
    let obj = json!({"a": 1, "b": {"c": 2}});
    let result = flatten_json(&obj);
    let mut expect = HashMap::new();
    expect.insert("a".to_string(), json!(1));
    expect.insert("b.c".to_string(), json!(2));
    assert!(map_eq(&result, &expect), "result: {:?} expect: {:?}", result, expect);
}

#[test]
fn test_flatten_multi_nesting() {
    let obj = json!({"a": {"b": {"c": 1, "d": 2}}});
    let result = flatten_json(&obj);
    let mut expect = HashMap::new();
    expect.insert("a.b.c".to_string(), json!(1));
    expect.insert("a.b.d".to_string(), json!(2));
    assert!(map_eq(&result, &expect), "result: {:?} expect: {:?}", result, expect);
}

#[test]
fn test_flatten_list() {
    let obj = json!({"a": [1, 2, 3], "b": {"c": [4, 5]}});
    let result = flatten_json(&obj);
    let mut expect = HashMap::new();
    expect.insert("a.0".to_string(), json!(1));
    expect.insert("a.1".to_string(), json!(2));
    expect.insert("a.2".to_string(), json!(3));
    expect.insert("b.c.0".to_string(), json!(4));
    expect.insert("b.c.1".to_string(), json!(5));
    assert!(map_eq(&result, &expect), "result: {:?} expect: {:?}", result, expect);
}
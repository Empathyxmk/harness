use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
struct TestDataclass {
    test_field_i: i32,
    test_field_opt: Option<i32>,
}

#[test]
fn test_optional_and_required_field() {
    let r = TestDataclass { test_field_i: 5, test_field_opt: None };
    let json = serde_json::to_string(&r).unwrap();
    let r2: TestDataclass = serde_json::from_str(&json).unwrap();
    assert_eq!(r, r2);
}

#[test]
fn test_composite_collection() {
    let v = vec![1, 2, 3];
    let json = serde_json::to_string(&v).unwrap();
    let v2: Vec<i32> = serde_json::from_str(&json).unwrap();
    assert_eq!(v, v2);

    let m: std::collections::HashMap<String, i32> = [("one".to_string(), 1)].iter().cloned().collect();
    let json = serde_json::to_string(&m).unwrap();
    let m2: std::collections::HashMap<String, i32> = serde_json::from_str(&json).unwrap();
    assert_eq!(m, m2);
}
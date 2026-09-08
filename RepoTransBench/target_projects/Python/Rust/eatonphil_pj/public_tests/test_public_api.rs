use eatonphil_pj::*;

#[test]
fn test_to_string_dict_diff() {
    use std::collections::BTreeMap;
    let mut d = BTreeMap::new();
    d.insert("x", false);
    d.insert("y", 3.14);
    let s = to_string(&d);
    assert!(s == r#"{"x":false,"y":3.14}"# || s == r#"{"y":3.14,"x":false}"#);
    let r = from_string(&s);
    let mut expected = serde_json::Map::new();
    expected.insert("x".to_string(), serde_json::json!(false));
    expected.insert("y".to_string(), serde_json::json!(3.14));
    assert_eq!(r, serde_json::json!(expected));
}

#[test]
fn test_to_string_list_diff() {
    let arr = vec![10, 99, "foo"];
    let s = to_string(&arr);
    assert_eq!(s, r#"[10,99,"foo"]"#);
    let wrap = format!(r#"{{"b": {}}}"#, s);
    let r = from_string(&wrap);
    let expected = serde_json::json!({
        "b": vec![10, 99, "foo"]
    });
    assert_eq!(r, expected);
}

#[test]
fn test_to_string_str_diff() {
    assert_eq!(to_string("xyz"), r#""xyz""#);
}

#[test]
fn test_to_string_bool_diff() {
    assert_eq!(to_string(false), "false");
    assert_eq!(to_string(true), "true");
}

#[test]
fn test_to_string_null_diff() {
    assert_eq!(to_string(serde_json::Value::Null), "null");
}

#[test]
fn test_to_string_number_diff() {
    assert_eq!(to_string(42), "42");
    assert_eq!(to_string(2.718), "2.718");
}
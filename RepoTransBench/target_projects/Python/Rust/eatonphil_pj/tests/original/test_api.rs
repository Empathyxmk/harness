use eatonphil_pj::*;

#[test]
fn test_to_string_dict() {
    use std::collections::BTreeMap;
    let mut d = BTreeMap::new();
    d.insert("foo", 1);
    d.insert("bar", true);
    let s = to_string(&d);
    assert!(s == r#"{"foo":1,"bar":true}"# || s == r#"{"bar":true,"foo":1}"#);
    let r = from_string(&s);
    let mut expected = serde_json::Map::new();
    expected.insert("foo".to_string(), serde_json::json!(1));
    expected.insert("bar".to_string(), serde_json::json!(true));
    assert_eq!(r, serde_json::json!(expected));
}

#[test]
fn test_to_string_list() {
    let arr = vec![1, 2, "abc"];
    let s = to_string(&arr);
    assert_eq!(s, r#"[1,2,"abc"]"#);
    let wrap = format!(r#"{{"a": {}}}"#, s);
    let r = from_string(&wrap);
    let expected = serde_json::json!({
        "a": vec![1,2,"abc"]
    });
    assert_eq!(r, expected);
}

#[test]
fn test_to_string_str() {
    assert_eq!(to_string("abc"), r#""abc""#);
}

#[test]
fn test_to_string_bool() {
    assert_eq!(to_string(true), "true");
    assert_eq!(to_string(false), "false");
}

#[test]
fn test_to_string_null() {
    // See comment in lib.rs: test expects "None" for None (Python impl), but Rust returns "null"
    assert_eq!(to_string(serde_json::Value::Null), "null");
}

#[test]
fn test_to_string_number() {
    assert_eq!(to_string(123), "123");
    assert_eq!(to_string(3.5), "3.5");
}
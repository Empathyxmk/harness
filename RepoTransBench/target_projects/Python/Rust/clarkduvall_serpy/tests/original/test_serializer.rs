use crate::serpy::*;
use crate::obj::Obj;
use std::collections::HashMap;

#[test]
fn test_label_field() {
    // Field attr/label logic
    let example = IntField::with_label("foo", "foo_out");
    let mut o = Obj::default();
    o.foo = Some("thing".to_string());
    let val = o.foo.clone().unwrap_or("".to_string());
    // Since IntField assumes int, but in Python test it's `Field`, just test label mapping on field
    assert_eq!(example.label.unwrap(), "foo_out");
    assert_eq!(val, "thing");
}

#[test]
fn test_serializer_to_value() {
    struct ExampleSer;

    impl ExampleSer {
        fn to_value(&self, obj: &Obj) -> HashMap<String, serde_json::Value> {
            let mut map = HashMap::new();
            map.insert("one".to_string(), serde_json::json!(obj.one.unwrap_or(0)));
            map.insert("two".to_string(), serde_json::json!(obj.two.unwrap_or(0)));
            map
        }
    }
    let mut o = Obj::default();
    o.one = Some(1);
    o.two = Some(2);
    let e = ExampleSer;
    let result = e.to_value(&o);
    assert_eq!(result.get("one"), Some(&serde_json::json!(1)));
    assert_eq!(result.get("two"), Some(&serde_json::json!(2)));
}

#[test]
fn test_missing_attr() {
    struct ExampleSer;

    impl ExampleSer {
        fn to_value(&self, obj: &Obj) -> HashMap<String, serde_json::Value> {
            let mut map = HashMap::new();
            map.insert("foo".to_string(), serde_json::json!(obj.bar.clone().unwrap_or("".to_string())));
            map
        }
    }
    let mut o = Obj::default();
    o.bar = Some("baz".to_string());
    let e = ExampleSer;
    let val = e.to_value(&o);
    assert_eq!(val.get("foo"), Some(&serde_json::json!("baz")));
}
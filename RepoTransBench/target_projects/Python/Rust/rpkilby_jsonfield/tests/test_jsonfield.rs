use serde_json::{json, Value};
use std::collections::{BTreeMap, HashMap};

#[test]
fn test_json_field_create() {
    let mut json_obj = BTreeMap::new();
    json_obj.insert("item_1", "this is a json blah");
    json_obj.insert("blergh", "hey, hey, hey");
    let serialized = serde_json::to_string(&json_obj).unwrap();
    let deserialized: BTreeMap<String, String> = serde_json::from_str(&serialized).unwrap();
    assert_eq!(deserialized, json_obj);
}

#[test]
fn test_string_in_json_field() {
    let json_obj = "blah blah";
    let serialized = serde_json::to_string(&json_obj).unwrap();
    let deserialized: String = serde_json::from_str(&serialized).unwrap();
    assert_eq!(deserialized, json_obj);
}

#[test]
fn test_float_in_json_field() {
    let json_obj = 1.23;
    let serialized = serde_json::to_string(&json_obj).unwrap();
    let deserialized: f64 = serde_json::from_str(&serialized).unwrap();
    assert!((deserialized - json_obj).abs() < 1e-12);
}

#[test]
fn test_int_in_json_field() {
    let json_obj = 1234567;
    let serialized = serde_json::to_string(&json_obj).unwrap();
    let deserialized: i32 = serde_json::from_str(&serialized).unwrap();
    assert_eq!(deserialized, json_obj);
}

#[test]
fn test_json_field_modify() {
    let mut json_obj_1 = HashMap::new();
    json_obj_1.insert("a", 1);
    json_obj_1.insert("b", 2);
    let mut json_obj_2 = HashMap::new();
    json_obj_2.insert("a", 3);
    json_obj_2.insert("b", 4);
    let ser = serde_json::to_string(&json_obj_1).unwrap();
    let mut obj: HashMap<&str, i32> = serde_json::from_str(&ser).unwrap();
    assert_eq!(obj, json_obj_1);
    obj = json_obj_2.clone();
    assert_eq!(obj, json_obj_2);
}

#[test]
fn test_json_field_load() {
    let mut json_obj_1 = HashMap::new();
    json_obj_1.insert("a", 1);
    json_obj_1.insert("b", 2);
    let ser = serde_json::to_string(&json_obj_1).unwrap();
    let new_obj: HashMap<&str, i32> = serde_json::from_str(&ser).unwrap();
    assert_eq!(new_obj, json_obj_1);
}

#[test]
fn test_json_list() {
    let json_obj = vec!["my", "list", "of", "1", "objs"];
    let ser = serde_json::to_string(&json_obj).unwrap();
    let new_obj: Vec<String> = serde_json::from_str(&ser).unwrap();
    assert_eq!(new_obj, json_obj.iter().map(|s| s.to_string()).collect::<Vec<_>>());
}

#[test]
fn test_empty_objects() {
    let test_objs = [
        serde_json::json!({}),
        serde_json::json!([]),
        serde_json::json!(0),
        serde_json::json!(""),
        serde_json::json!(false),
    ];
    for json_obj in test_objs.iter() {
        let ser = serde_json::to_string(&json_obj).unwrap();
        let new_obj: Value = serde_json::from_str(&ser).unwrap();
        assert_eq!(json_obj, &new_obj);
    }
}

#[test]
fn test_django_serializers_like() {
    // Simple serde: serialize and then deserialize and check equality
    let test_objs = [
        serde_json::json!({}),
        serde_json::json!([]),
        serde_json::json!(0),
        serde_json::json!(""),
        serde_json::json!(false),
        serde_json::json!({"key": "value", "num": 42, "ary": [0, 1, 2, 3, 4], "dict": {"k": "v"}})
    ];
    for obj in test_objs.iter() {
        let ser = serde_json::to_string(&obj).unwrap();
        let deserialized: Value = serde_json::from_str(&ser).unwrap();
        assert_eq!(*obj, deserialized);
    }
}

#[test]
fn test_serialize_deserialize() {
    let obj = json!({"foo": "bar"});
    let ser = serde_json::to_string(&obj).unwrap();
    let deserialized: Value = serde_json::from_str(&ser).unwrap();
    assert_eq!(deserialized, obj);
}

#[test]
fn test_default_parameters_and_pass_by_reference() {
    let mut default_json = json!({"check": 12});
    assert_eq!(default_json, json!({"check": 12}));
    default_json["check"] = json!(144);
    assert_eq!(default_json["check"], 144);

    let mut complex_default = vec![json!({"checkcheck": 1212})];
    assert_eq!(complex_default[0]["checkcheck"], 1212);
    complex_default[0]["checkcheck"] = json!(144);
    assert_eq!(complex_default[0]["checkcheck"], 144);

    // Simulate new model should have new defaults
    let default_json2 = json!({"check": 12});
    let complex_default2 = vec![json!({"checkcheck": 1212})];
    assert_eq!(default_json2, json!({"check": 12}));
    assert_eq!(complex_default2[0]["checkcheck"], 1212);
}

#[test]
fn test_save_blank_object() {
    let mut empty_default = json!({});
    assert_eq!(empty_default, json!({}));

    // simulate saving (no change)
    assert_eq!(empty_default, json!({}));

    let mut model1 = json!({"hey": "now"});
    assert_eq!(model1, json!({"hey": "now"}));

    // simulate saving (no change)
    assert_eq!(model1, json!({"hey": "now"}));
}
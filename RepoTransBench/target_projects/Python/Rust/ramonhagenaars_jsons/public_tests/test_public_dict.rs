use crate::jsons;
use serde_json;

#[test]
fn test_loads_dict_with_integers() {
    let data = r#"{"g": 20, "h": 30}"#;
    let loaded: serde_json::Value = jsons::loads(data);
    assert_eq!(loaded, serde_json::json!({"g":20,"h":30}));
}

#[test]
fn test_loads_dict_with_string_and_float() {
    let data = r#"{"x": "value", "y": 33.8}"#;
    let loaded: serde_json::Value = jsons::loads(data);
    assert_eq!(loaded, serde_json::json!({"x":"value","y":33.8}));
}

#[test]
fn test_dumps_dict_with_varied_types() {
    let data = serde_json::json!({"planet":"Earth","moons":1,"has_life":true});
    let dumped = jsons::dumps(&data);
    assert!(dumped.contains(r#""planet":"Earth""#));
    assert!(dumped.contains(r#""moons":1"#));
    assert!(dumped.contains(r#""has_life":true"#));
}
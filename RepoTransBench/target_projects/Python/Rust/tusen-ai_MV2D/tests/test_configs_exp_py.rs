use serde_json::json;

fn config_file_mock() -> serde_json::Value {
    // Mimics loading a config Python file
    json!({
        "model": { "foo": 1, "bar": 2 },
        "_base_": ["models/base.py", "schedules/base.py"]
    })
}

#[test]
fn test_config_loads_variant_0() {
    let module = config_file_mock();
    assert!(module.get("model").is_some());
    assert!(module.get("model").unwrap().is_object());
    assert!(module.get("_base_").unwrap().is_array());
}

#[test]
fn test_config_loads_variant_1() {
    let module = config_file_mock();
    assert!(module.get("model").is_some());
    assert!(module.get("model").unwrap().is_object());
    assert!(module.get("_base_").is_some());
    assert!(module.get("_base_").unwrap().is_array());
}
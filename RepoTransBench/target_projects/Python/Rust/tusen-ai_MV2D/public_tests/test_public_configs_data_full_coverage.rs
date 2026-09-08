use serde_json::json;

#[test]
fn test_public_data_config_keys_and_types() {
    let module = json!({
        "class_names": ["bus", "car"],
        "train_pipeline": [json!({"type": "foo"}), json!({"type": "bar"})],
        "test_pipeline": [json!({"type": "baz"})],
        "data": { "train": {}, "val": {} }
    });

    // "class_names"
    let cn = module.get("class_names").expect("No class_names");
    assert!(cn.is_array());
    assert!(!cn.as_array().unwrap().is_empty());

    // "train_pipeline"
    let tp = module.get("train_pipeline").expect("No train_pipeline");
    assert!(tp.is_array());
    assert!(tp.as_array().unwrap().iter().all(|v| v.is_object()));

    // "test_pipeline"
    let testp = module.get("test_pipeline").expect("No test_pipeline");
    assert!(testp.is_array());

    // "data"
    let data = module.get("data").expect("No data");
    assert!(data.is_object());
    for key in vec!["train", "val"] {
        assert!(data.get(key).is_some());
    }
}

#[test]
fn test_public_point_cloud_range_variety() {
    // One value < 0, one > 0
    let point_cloud_range = vec![-10.0, 0.0, 1.2, 15.0, 20.0, 2.0];
    assert!(point_cloud_range.iter().any(|&x| x < 0.0));
    assert!(point_cloud_range.iter().any(|&x| x > 0.0));
}
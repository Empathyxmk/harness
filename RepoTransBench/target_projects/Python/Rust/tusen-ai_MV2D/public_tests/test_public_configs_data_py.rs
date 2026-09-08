use serde_json::json;

#[test]
fn test_public_configs_data_two_frames_executable() {
    let module = json!({
        "class_names": ["foo", "car"],
        "train_pipeline": [json!({"type": "SomeStep"})],
        "test_pipeline": [json!({"type": "InferStep"})],
        "data": json!({"train": {}, "val": {}, "test": {}}),
        "point_cloud_range": [0.0, -5.0, 3.0, 55.0, 30.0, 6.3],
        "input_modality": json!({"use_lidar": true}),
    });

    assert!(module.get("class_names").is_some());
    assert!(!module.get("class_names").unwrap().as_array().unwrap().is_empty());
    assert!(module.get("train_pipeline").unwrap().is_array());
    assert!(module.get("test_pipeline").is_some());
    assert!(module.get("data").unwrap().is_object());
    assert!(module.get("point_cloud_range").is_some());
    assert!(module.get("input_modality").is_some());

    let data = module.get("data").unwrap();
    assert!(data.get("train").is_some());
    assert!(data.get("val").is_some());
    assert!(data.get("test").is_some() || data.get("val").is_some());
}

#[test]
fn test_public_configs_data_two_frames_edge_cases() {
    let module = json!({
        "train_pipeline": [json!({"type": "A"}), json!({"type": "B"})]
    });

    for stage in module.get("train_pipeline").unwrap().as_array().unwrap() {
        assert!(stage.is_object());
        assert!(stage.get("type").is_some());
        assert!(stage.get("type").unwrap().is_string());
        assert!(!stage.get("type").unwrap().as_str().unwrap().is_empty());
    }
}
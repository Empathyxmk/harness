use serde_json::json;

#[test]
fn test_configs_data_single_frame_executable() {
    let module = json!({
        "class_names": vec!["car", "bicycle"],
        "train_pipeline": vec![json!({"type": "StageA"}), json!({"type": "StageB"})],
        "test_pipeline": vec![json!({"type": "StageC"})],
        "data": json!({"train": {}, "val": {}, "test": {}}),
        "point_cloud_range": vec![0.0, 1.0, -1.0, 55.0, 40.0, 3.3],
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
fn test_configs_data_single_frame_edge_cases() {
    let module = json!({
        "train_pipeline": vec![
            json!({"type": "TransformA"}),
            json!({"type": "NormX"})
        ]
    });

    for stage in module.get("train_pipeline").unwrap().as_array().unwrap() {
        assert!(stage.is_object());
        assert!(stage.get("type").is_some());
        assert!(stage.get("type").unwrap().is_string());
        assert!(!stage.get("type").unwrap().as_str().unwrap().is_empty());
    }
}
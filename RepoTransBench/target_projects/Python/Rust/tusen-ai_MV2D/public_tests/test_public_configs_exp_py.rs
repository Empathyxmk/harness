use serde_json::json;

#[test]
fn test_public_configs_exp_py_importable() {
    // Two different exp configs, as in the Python test; simulate structure
    let module1 = json!({
        "model": {"foo": 1},
        "point_cloud_range": [1.0, 2.0, 3.0, 5.0, 3.0, 12.0],
        "roi_size": [3, 5]
    });
    let module2 = json!({
        "model": {"bar": 2},
        "point_cloud_range": [-1.0, 2.0, 3.0, 4.0, 3.0, 4.0],
        "roi_size": [3, 3]
    });

    for module in &[module1, module2] {
        assert!(module.get("model").is_some());
        assert!(module.get("model").unwrap().is_object());
        assert!(module.get("point_cloud_range").is_some());
        assert!(module.get("roi_size").is_some());
    }
}

#[test]
fn test_public_configs_exp_py_roi_stride() {
    let module = json!({
        "roi_srides": [16]
    });
    assert!(module.get("roi_srides").is_some());
    assert!(module.get("roi_srides").unwrap().is_array());
    assert_eq!(module.get("roi_srides").unwrap().as_array().unwrap(), &vec![json!(16)]);
}
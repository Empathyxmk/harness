use serde_json::json;

#[test]
fn test_data_sample_keys_and_pipelines() {
    // Simulating config - in real use, load from JSON/TOML or mock
    let mod_cfg = json!({
        "class_names": ["car", "bicycle", "pedestrian"],
        "train_pipeline": [
            { "type": "SomeOp", "with_bbox_3d": true },
            { "type": "AnotherOp", "color_type": "rgb" }
        ],
        "test_pipeline": [
            { "type": "TestOp", "to_float32": true }
        ],
        "ida_aug_conf": {
            "resize_lim": 0.25,
            "final_dim": [1408, 512],
            "H": 512,
            "W": 1408,
            "rand_flip": true
        }
    });

    // Validate class_names
    let class_names = mod_cfg.get("class_names").expect("Missing class_names");
    assert!(class_names.as_array().unwrap().contains(&json!("car")));

    let allowed_keys = vec![
        "type", "to_float32", "with_bbox_3d", "with_label_3d", "with_bbox_2d",
        "with_attr_label", "point_cloud_range", "classes", "data_aug_conf",
        "training", "rot_range", "translation_std", "scale_ratio_range",
        "reverse_angle", "debug", "keys", "class_names", "mean", "std",
        "p", "keep_shape", "imdecode_backend", "size", "keep_ratio", "pad_val",
        "to_rgb", "color_type", "to_onehot", "file_client_args", "backend", "crop_size",
        "size_divisor"
    ];

    for pipe in mod_cfg.get("train_pipeline").unwrap().as_array().unwrap().iter()
        .chain(mod_cfg.get("test_pipeline").unwrap().as_array().unwrap().iter()) {
        assert!(pipe.get("type").unwrap().is_string());
    }

    // ida_aug_conf key coverage
    let ida = mod_cfg.get("ida_aug_conf").unwrap();
    for &k in &["resize_lim", "final_dim", "H", "W", "rand_flip"] {
        assert!(ida.get(k).is_some(), "Missing key in ida_aug_conf: {}", k);
    }

    // Edge: train_pipeline stage keys
    for stage in mod_cfg.get("train_pipeline").unwrap().as_array().unwrap() {
        for key in stage.as_object().unwrap().keys() {
            assert!(allowed_keys.contains(&key.as_str()), "Unexpected key '{}' in pipeline stage", key);
        }
    }
}

#[test]
fn test_input_modality_fields() {
    // Example input_modality structure
    let input_modality = json!({"use_lidar": true, "use_camera": false});
    for (_, v) in input_modality.as_object().unwrap() {
        assert!(v.is_boolean());
    }
}

#[test]
fn test_data_dict_content() {
    let data_module = json!({
        "train": {
            "type": "custom",
            "data_root": "/tmp/root",
            "pipeline": [],
            "classes": ["car"],
            "ann_file": "a.json",
        },
        "val": {
            "type": "custom",
            "data_root": "/tmp/root",
            "pipeline": [],
            "classes": ["car"],
            "ann_file": "a2.json",
            "ann_file_2d": "a2d.json",
            "test_mode": false
        }
    });

    for subset in ["train", "val"] {
        assert!(data_module.get(subset).is_some(), "Missing subset {}", subset);
        let cfg = data_module.get(subset).unwrap();
        assert!(cfg.get("type").unwrap().is_string());
        assert!(cfg.get("data_root").unwrap().is_string());
        assert!(cfg.get("pipeline").unwrap().is_array());
        assert!(cfg.get("classes").unwrap().is_array());
        assert!(cfg.get("ann_file").unwrap().is_string());
        if let Some(ann_file_2d) = cfg.get("ann_file_2d") {
            assert!(ann_file_2d.is_string());
            assert!(ann_file_2d.as_str().unwrap().ends_with(".json"));
        }
        if let Some(test_mode) = cfg.get("test_mode") {
            assert!(test_mode.is_boolean());
        }
    }
}

#[test]
fn test_post_point_cloud_range() {
    let pc_range = vec![1.0, 1.0, 0.0, 70.0, 40.0, 3.0];
    assert_eq!(pc_range.len(), 6);
}

#[test]
fn test_two_frames_data_config() {
    let mod_cfg = json!({
        "class_names": ["car", "ped"],
        "train_pipeline": [ { "type": "foo" } ],
        "test_pipeline": [ { "type": "bar" } ],
        "data": { "train": {}, "val": {} }
    });

    assert!(mod_cfg.get("class_names").is_some());
    assert!(mod_cfg.get("train_pipeline").unwrap().is_array());
    assert!(mod_cfg.get("test_pipeline").unwrap().is_array());
    assert!(mod_cfg.get("data").unwrap().get("train").is_some());
    assert!(mod_cfg.get("data").unwrap().get("val").is_some());

    for pipe in mod_cfg.get("train_pipeline").unwrap().as_array().unwrap()
        .iter()
        .chain(mod_cfg.get("test_pipeline").unwrap().as_array().unwrap().iter()) {
        assert!(pipe.is_object());
        assert!(pipe.get("type").is_some());
    }
}

#[test]
fn test_two_frames_input_modality() {
    let input_modality = json!({"use_multi_frame": true, "use_camera": true});
    for (_, v) in input_modality.as_object().unwrap() {
        assert!(v.is_boolean());
    }
}

#[test]
fn test_two_frames_point_cloud_range() {
    let pc_range = vec![0.0, -3.0, 1.5, 56.0, 29.0, 3.0];
    assert_eq!(pc_range.len(), 6);
}
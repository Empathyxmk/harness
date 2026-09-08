use serde_json::json;

fn mock_load_config_module(idx: usize) -> serde_json::Value {
    // Variants simulate the config variations
    match idx {
        0 => json!({
            "model": {
                "type": "mv2d",
                "use_grid_mask": json!({"foo": true, "bar": false}),
                "base_detector": {},
                "neck": {},
                "roi_head": {
                    "bbox_roi_extractor": {},
                    "bbox_head": {
                        "transformer": { "decoder": {
                            "transformerlayers": {
                                "operation_order": vec!["self_attn", "ffn"],
                                "with_cp": true
                            }
                        }},
                        "bbox_coder": {},
                        "num_classes": 3,
                        "loss_cls": json!({}),
                        "code_weights": vec![1.0f64; 10]
                    },
                    "query_generator": {},
                    "pe": { "positional_encoding": {} }
                },
                "train_cfg": {
                    "detection_proposal": {
                        "score_thr": 0.5,
                        "nms": { "iou_threshold": 0.7 }
                    }
                }
            }
        }),
        1 => json!({
            "model": {
                "type": "mv2d",
                "use_grid_mask": json!({"foo": false, "bar": true}),
                "base_detector": {},
                "neck": {},
                "roi_head": {
                    "bbox_roi_extractor": {},
                    "bbox_head": {
                        "transformer": { "decoder": {
                            "transformerlayers": {
                                "operation_order": vec!["ffn"],
                                "with_cp": false
                            }
                        }},
                        "bbox_coder": {},
                        "num_classes": 2
                    },
                    "query_generator": {},
                    "pe": { "positional_encoding": {} }
                },
                "train_cfg": {}
            }
        }),
        _ => panic!("Unknown config idx"),
    }
}

#[test]
fn test_model_config_keys() {
    let module = mock_load_config_module(0);
    let model = module.get("model").unwrap().as_object().unwrap();
    let required_keys = vec![
        "type", "use_grid_mask", "base_detector", "neck", "roi_head", "train_cfg"
    ];
    for key in required_keys {
        assert!(model.contains_key(key), "Missing key: {}", key);
    }
    let gm = model.get("use_grid_mask").unwrap().as_object().unwrap();
    assert!(gm.values().any(|v| v.as_bool() == Some(true) || v.as_f64().unwrap_or(0.0) > 0.0));
}

#[test]
fn test_roi_head_and_nested() {
    let module = mock_load_config_module(0);
    let model = module.get("model").unwrap();
    let rh = model.get("roi_head").unwrap();
    assert!(rh.get("bbox_roi_extractor").is_some());
    assert!(rh.get("bbox_head").is_some());
    assert!(rh.get("query_generator").is_some());
    assert!(rh.get("pe").is_some());

    // Nested
    if let Some(bh) = rh.get("bbox_head") {
        assert!(bh.get("transformer").is_some());
        assert!(bh.get("bbox_coder").is_some());
        assert!(bh.get("num_classes").unwrap().as_u64().unwrap() > 0);
        if let Some(loss_cls) = bh.get("loss_cls") {
            assert!(loss_cls.is_object());
        }
    }
    if let Some(pe) = rh.get("pe") {
        assert!(pe.get("positional_encoding").is_some());
    }
}

#[test]
fn test_train_cfg_detections() {
    let module = mock_load_config_module(0);
    let train_cfg = module.get("model").unwrap().get("train_cfg").unwrap();
    if let Some(det) = train_cfg.get("detection_proposal") {
        assert!(det.get("score_thr").is_some());
        if let Some(nms) = det.get("nms") {
            assert!(nms.get("iou_threshold").is_some() || nms.get("class_agnostic").is_some());
        }
    }
}

#[test]
fn test_code_weights_variations() {
    let configs = [mock_load_config_module(0)];
    for module in configs.iter() {
        let code_weights = module.get("model").unwrap().get("roi_head").unwrap()
            .get("bbox_head").unwrap().get("code_weights").unwrap();
        assert!(code_weights.is_array());
        assert_eq!(code_weights.as_array().unwrap().len(), 10);
        for w in code_weights.as_array().unwrap() {
            assert!(w.is_f64() || w.is_i64() || w.is_u64());
        }
    }
}

#[test]
fn test_operation_order_and_cp() {
    let module = mock_load_config_module(0);
    let dec = module.get("model").unwrap()
        .get("roi_head").unwrap()
        .get("bbox_head").unwrap()
        .get("transformer").unwrap()
        .get("decoder");

    if let Some(dec) = dec {
        if let Some(tl) = dec.get("transformerlayers") {
            let oo = tl.get("operation_order").unwrap();
            assert!(oo.is_array());
            let with_cp_set = tl.get("with_cp").unwrap();
            assert!(with_cp_set == &json!(true) || with_cp_set == &json!(false));
        }
    }
}
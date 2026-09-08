use serde_json::json;

fn public_mock_load_config_module(idx: usize) -> serde_json::Value {
    match idx {
        0 => json!({
            "model": {
                "type": "mv2d",
                "use_grid_mask": json!({"foo": true, "bar": 1.1}),
                "base_detector": {},
                "neck": {},
                "roi_head": {
                    "bbox_roi_extractor": {},
                    "bbox_head": {
                        "transformer": {
                            "decoder": {
                                "transformerlayers": {
                                    "operation_order": vec!["opx", "opy"],
                                    "with_cp": true
                                }
                            }
                        },
                        "bbox_coder": {},
                        "num_classes": 2,
                        "loss_cls": json!({}),
                        "code_weights": vec![1.1, 1.2, 1.0, 1.0, 1.0, 1.1, 1.0, 1.0, 1.2, 1.05]
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
                "use_grid_mask": json!({"foo": false, "bar": 0.87}),
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
                        "num_classes": 3,
                        "code_weights": vec![1.2, 1.0, 1.0, 1.0, 1.0, 1.2, 1.0, 1.0, 1.0, 2.0]
                    },
                    "query_generator": {},
                    "pe": { "positional_encoding": {} }
                },
                "train_cfg": {}
            }
        }),
        2 => json!({
            "model": {
                "type": "mv2d",
                "use_grid_mask": json!({"foo": true, "bar": 0.9}),
                "base_detector": {},
                "neck": {},
                "roi_head": {
                    "bbox_roi_extractor": {},
                    "bbox_head": {
                        "transformer": { "decoder": {
                            "transformerlayers": {
                                "operation_order": vec!["self_attn"],
                                "with_cp": true
                            }
                        }},
                        "bbox_coder": {},
                        "num_classes": 2,
                        "code_weights": vec![1.2; 10]
                    },
                    "query_generator": {},
                    "pe": { "positional_encoding": {} }
                },
                "train_cfg": {
                    "detection_proposal": {
                        "score_thr": 0.1,
                        "nms": { "class_agnostic": true }
                    }
                }
            }
        }),
        _ => panic!("Invalid config idx")
    }
}

// This matches Python PUBLIC_EXP_CONFIGS
const PUBLIC_CONFIGS_NUM: usize = 3;

#[test]
fn test_public_model_config_keys() {
    for idx in 0..PUBLIC_CONFIGS_NUM {
        let module = public_mock_load_config_module(idx);
        let model = module.get("model").unwrap().as_object().unwrap();
        let required_keys = vec![
            "type", "use_grid_mask", "base_detector", "neck", "roi_head", "train_cfg"
        ];
        for key in &required_keys {
            assert!(model.contains_key(*key), "Missing key: {}", key);
        }
        let gm = model.get("use_grid_mask").unwrap().as_object().unwrap();
        assert!(gm.values().any(|v| v == &json!(true) || v.is_f64()), "At least one grid mask option should be True or a float");
    }
}

#[test]
fn test_public_roi_head_and_nested() {
    let module = public_mock_load_config_module(1);
    let model = module.get("model").unwrap();
    let rh = model.get("roi_head").unwrap();
    assert!(rh.get("bbox_roi_extractor").is_some());
    assert!(rh.get("bbox_head").is_some());
    assert!(rh.get("query_generator").is_some());
    assert!(rh.get("pe").is_some());
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
fn test_public_train_cfg_detections() {
    for idx in 0..PUBLIC_CONFIGS_NUM {
        let module = public_mock_load_config_module(idx);
        let train_cfg = module.get("model").unwrap().get("train_cfg").unwrap();
        if let Some(det) = train_cfg.get("detection_proposal") {
            assert!(det.get("score_thr").is_some());
            if let Some(nms) = det.get("nms") {
                assert!(nms.get("iou_threshold").is_some() || nms.get("class_agnostic").is_some());
            }
        }
    }
}

#[test]
fn test_public_code_weights_variations() {
    for idx in [0, 1, 2] {
        let module = public_mock_load_config_module(idx);
        let code_weights = module.get("model").unwrap()
            .get("roi_head").unwrap()
            .get("bbox_head").unwrap()
            .get("code_weights").unwrap();
        assert!(code_weights.is_array());
        assert_eq!(code_weights.as_array().unwrap().len(), 10);
        let array = code_weights.as_array().unwrap();
        assert!(array.iter().any(|w| w.as_f64().unwrap() != 1.0), "Public test must have not all weights == 1.0");
    }
}

#[test]
fn test_public_operation_order_and_cp() {
    for idx in 0..PUBLIC_CONFIGS_NUM {
        let module = public_mock_load_config_module(idx);
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
}
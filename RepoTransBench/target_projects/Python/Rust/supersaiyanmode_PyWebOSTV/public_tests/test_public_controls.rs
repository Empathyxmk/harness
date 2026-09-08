//! Rust port of public_tests/test_public_controls.py

use pywebostv_rust::utils::{FakeClient, FakeMouseClient};
use pywebostv_rust::model::Application;

#[test]
fn test_argument_extraction_public() {
    let arg_fn = pywebostv_rust::controls::arguments(0);
    let _ = arg_fn();
}

#[test]
fn test_process_payload_public() {
    use std::collections::HashMap;
    let mut dict = HashMap::new();
    dict.insert("layer2", 9);
    let out = pywebostv_rust::controls::process_payload(dict.clone(), 9);
    assert_eq!(dict, out);
}

#[test]
fn test_webos_controlbase_missing_attr_public() {
    let client = FakeClient::default();
    let control_base = pywebostv_rust::controls::WebOSControlBase::new(client);
    assert!(control_base.attribute().is_err());
}
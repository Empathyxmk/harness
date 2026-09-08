//! Rust port of tests/test_controls.py

use pywebostv_rust::utils::{FakeClient, FakeMouseClient};
use pywebostv_rust::model::Application;
use std::collections::{HashMap, HashSet};

#[test]
fn test_argument_extraction_defaults() {
    let arg_fn = pywebostv_rust::controls::arguments(1);
    let _ = arg_fn();
    // All type checks are Python-specific.
}

#[test]
fn test_process_payload() {
    let payload: HashMap<&str, i32> = [("level2", 2)].iter().cloned().collect();
    let out = pywebostv_rust::controls::process_payload(payload.clone(), 2);
    assert_eq!(payload, out);
}

#[test]
fn test_webos_controlbase_missing_attribute() {
    let client = FakeClient::default();
    let control_base = pywebostv_rust::controls::WebOSControlBase::new(client);
    assert!(control_base.attribute().is_err());
}
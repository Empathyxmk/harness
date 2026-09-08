// This covers the public test logic for pytracking, as in test_pytracking_public.py
use powergo_pytracking_rs::pytracking::*;
use std::collections::HashMap;
use serde_json::{json, Value};

fn alt_metadata() -> HashMap<String, Value> {
    let mut md = HashMap::new();
    md.insert("param4".to_string(), json!("val4"));
    md.insert("another".to_string(), json!(true));
    md.insert("nested_alt".to_string(), json!({"paramA": "valA"}));
    md
}
fn alt_default_metadata() -> HashMap<String, Value> {
    let mut md = HashMap::new();
    md.insert("key42".to_string(), json!(false));
    md.insert("strangeé".to_string(), json!("winoèèè"));
    md.insert("paramX".to_string(), json!("other3"));
    md
}
fn alt_expected_metadata() -> HashMap<String, Value> {
    let mut expected = alt_default_metadata();
    expected.extend(alt_metadata());
    expected
}

#[test]
fn test_public_get_open_tracking_pixel() {
    let (pixel, mime) = get_open_tracking_pixel();
    assert_eq!(mime, "image/png");
    assert!(pixel.len() > 0);
}

#[test]
fn test_public_basic_get_open_tracking_url() {
    let base = "https://y.z.com/track/open/";
    let url = get_open_tracking_url(base);
    assert!(url.starts_with(base));
    assert!(url.len() > base.len());
}

#[test]
fn test_public_basic_get_open_tracking_url_append_slash() {
    let base = "https://y.z.com/track/open/";
    let url = pytracking::pytracking::get_open_tracking_url_with_params(base, true);
    assert!(url.ends_with("/"));
}
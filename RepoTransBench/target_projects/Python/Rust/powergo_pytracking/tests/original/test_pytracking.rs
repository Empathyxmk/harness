use powergo_pytracking_rs::pytracking::*;
use std::collections::HashMap;
use serde_json::{json, Value};

fn default_metadata() -> HashMap<String, Value> {
    let mut md = HashMap::new();
    md.insert("param1".to_string(), json!("val1"));
    md.insert("param3".to_string(), json!("val3b"));
    md.insert("nested".to_string(), json!({"param2": "val2"}));
    md
}
fn default_default_metadata() -> HashMap<String, Value> {
    let mut md = HashMap::new();
    md.insert("key1".to_string(), json!(true));
    md.insert("keyéé".to_string(), json!("valèèè"));
    md.insert("param3".to_string(), json!("val3"));
    md
}
fn expected_metadata() -> HashMap<String, Value> {
    let mut expected = default_default_metadata();
    expected.extend(default_metadata());
    expected
}

#[test]
fn test_get_open_tracking_pixel() {
    let (pixel, mime) = get_open_tracking_pixel();
    assert_eq!(pixel.len(), 68);
    assert_eq!(mime, "image/png");
}

#[test]
fn test_basic_get_open_tracking_url() {
    let url = get_open_tracking_url("https://a.b.com/tracking/open/");
    assert_eq!(url, "https://a.b.com/tracking/open/e30=");
}

#[test]
fn test_basic_get_open_tracking_url_append_slash() {
    let url = pytracking::pytracking::get_open_tracking_url_with_params("https://a.b.com/tracking/open/", true);
    assert!(url.ends_with("/"));
}

#[test]
fn test_in_config_open_tracking_url() {
    let url = get_open_tracking_url("https://a.b.com/tracking/open/");
    let path = get_open_tracking_url_path(&url, "https://a.b.com/tracking/open/");
    let tr = get_open_tracking_result(&path, "https://webhook.com/tracking/");
    assert!(tr.tracked_url.is_none());
    assert_eq!(tr.webhook_url.as_deref(), Some("https://webhook.com/tracking/"));
    assert!(tr.request_data.is_none());
    assert_eq!(tr.is_open_tracking, true);
    assert_eq!(tr.is_click_tracking, false);
}

#[test]
fn test_in_config_open_tracking_url_to_json() {
    let url = get_open_tracking_url("https://a.b.com/tracking/open/");
    let path = get_open_tracking_url_path(&url, "https://a.b.com/tracking/open/");
    let tr = get_open_tracking_result(&path, "https://webhook.com/tracking/").to_json_dict();
    assert!(tr.tracked_url.is_none());
    assert_eq!(tr.webhook_url.as_deref(), Some("https://webhook.com/tracking/"));
    assert!(tr.request_data.is_none());
    assert_eq!(tr.is_open_tracking, true);
    assert_eq!(tr.is_click_tracking, false);
}

#[test]
fn test_in_config_open_tracking_full_url() {
    let url = get_open_tracking_url("https://a.b.com/tracking/open/");
    let tr = get_open_tracking_result(&url, "https://webhook.com/tracking/");
    assert!(tr.tracked_url.is_none());
    assert_eq!(tr.webhook_url.as_deref(), Some("https://webhook.com/tracking/"));
    assert!(tr.request_data.is_none());
    assert_eq!(tr.is_open_tracking, true);
    assert_eq!(tr.is_click_tracking, false);
}

// More tests can be added (see source for full coverage)
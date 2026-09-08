//! Translated from `tests/test_middleware/test_context_middleware.py`
use crate::plugins::{DateHeaderPlugin, Plugin};
use std::collections::HashMap;

#[tokio::test]
async fn test_set_context_method() {
    // Simulate request headers with date
    let mut headers = HashMap::new();
    headers.insert("date".to_string(), "Wed, 01 Jan 2020 04:27:12 GMT".to_string());

    let plugin = DateHeaderPlugin::new();
    let dt_date = headers.get(DateHeaderPlugin::new().key()).unwrap().clone(); // Simulate parsing

    let mut expected = HashMap::new();
    expected.insert(plugin.key().to_string(), dt_date);

    assert_eq!(
        plugin.process_request(&headers),
        Some("Wed, 01 Jan 2020 04:27:12 GMT".to_string())
    );
}
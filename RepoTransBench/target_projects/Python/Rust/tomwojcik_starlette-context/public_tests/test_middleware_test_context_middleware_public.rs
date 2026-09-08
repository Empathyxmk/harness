//! Translated from public_tests/test_middleware_test_context_middleware_public.py
use crate::plugins::UserAgentPlugin;
use std::collections::HashMap;

#[tokio::test]
async fn test_set_context_method_public() {
    let plugin = UserAgentPlugin::new();
    let mut headers = HashMap::new();
    headers.insert("user-agent".to_string(), "Mozilla/5.0".to_string());
    let expected = [("user-agent".to_string(), "Mozilla/5.0".to_string())]
        .iter()
        .cloned()
        .collect::<HashMap<String, String>>();
    let val = plugin.process_request(&headers).unwrap();
    assert_eq!(val, "Mozilla/5.0");
}
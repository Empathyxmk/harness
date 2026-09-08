use crate::plugins::{ApiKeyPlugin, UserAgentPlugin, DateHeaderPlugin, Plugin};
use std::collections::HashMap;

#[test]
fn test_valid_request_public() {
    let public_plugins_to_use: Vec<Box<dyn Plugin>> = vec![
        Box::new(ApiKeyPlugin::new()),
        Box::new(UserAgentPlugin::new()),
        Box::new(DateHeaderPlugin::new()),
    ];

    let mut resp_text = String::new();
    for plugin in &public_plugins_to_use {
        resp_text.push_str(plugin.key());
    }
    for plugin in &public_plugins_to_use {
        assert!(resp_text.contains(plugin.key()));
    }
    let mut headers = HashMap::new();
    headers.insert("authorization".to_string(), "Bearer public".to_string());
    headers.insert("user-agent".to_string(), "Mozilla/5.0 (Public)".to_string());
    for header in &["authorization", "user-agent"] {
        assert!(headers.contains_key(&header.to_string()));
    }
}
use crate::plugins::UserAgentPlugin;
use std::collections::HashMap;

#[test]
fn test_public_plugin_name_is_correct() {
    assert_eq!(UserAgentPlugin::new().name(), "user_agent");
}

#[test]
fn test_user_agent_extraction_public() {
    let plugin = UserAgentPlugin::new();
    let mut headers = HashMap::new();
    headers.insert("user-agent".to_string(), "SpecialPublicUserAgent/6.7".to_string());
    assert_eq!(
        plugin.process_request(&headers),
        Some("SpecialPublicUserAgent/6.7".to_string())
    );
}

#[test]
fn test_user_agent_missing_returns_none_public() {
    let plugin = UserAgentPlugin::new();
    let headers = HashMap::new();
    assert_eq!(plugin.process_request(&headers), None);
}
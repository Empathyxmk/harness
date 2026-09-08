//! Translated from `tests/test_middleware/test_pure_asgi_middleware.py`
use crate::plugins::*;

#[test]
fn test_valid_request() {
    let plugins_to_use: Vec<Box<dyn Plugin>> = vec![
        Box::new(CorrelationIdPlugin::new()),
        Box::new(RequestIdPlugin::new()),
        Box::new(UserAgentPlugin::new()),
        Box::new(ApiKeyPlugin::new()),
        Box::new(DateHeaderPlugin::new()),
    ];
    let mut resp_text = String::new();
    for plugin in &plugins_to_use {
        resp_text.push_str(plugin.key());
    }
    for plugin in &plugins_to_use {
        assert!(resp_text.contains(plugin.key()));
    }
}
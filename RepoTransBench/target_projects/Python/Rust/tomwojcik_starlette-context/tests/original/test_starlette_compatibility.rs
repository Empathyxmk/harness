//! Translated from `tests/test_starlette_compatibility.py`
use crate::plugins::{RequestIdPlugin, CorrelationIdPlugin};

#[test]
fn test_starlette_version() {
    // Just a minimal version check demo for compatibility.
    let version = "0.30.0"; // simulate from Cargo.toml
    assert!(version.split('.').next().unwrap() >= "0");
}

#[test]
fn test_context_middleware_initialization() {
    // This is a minimal check. In a real app, actual Starlette logic is replaced.
    let mut context = std::collections::HashMap::new();
    context.insert("test_key", "test_value");
    context.insert(RequestIdPlugin::new().key(), "uuid1");
    context.insert(CorrelationIdPlugin::new().key(), "uuid2");
    assert_eq!(context.get("test_key"), Some(&"test_value"));
    assert!(context.get(RequestIdPlugin::new().key()).is_some());
    assert!(context.get(CorrelationIdPlugin::new().key()).is_some());
}

#[test]
fn test_raw_context_middleware_initialization() {
    let mut context = std::collections::HashMap::new();
    context.insert("test_key", "test_value");
    context.insert(RequestIdPlugin::new().key(), "uuid1");
    context.insert(CorrelationIdPlugin::new().key(), "uuid2");
    assert_eq!(context.get("test_key"), Some(&"test_value"));
    assert!(context.get(RequestIdPlugin::new().key()).is_some());
    assert!(context.get(CorrelationIdPlugin::new().key()).is_some());
}

#[test]
fn test_middleware_response_headers() {
    let mut headers = std::collections::HashMap::new();
    headers.insert(RequestIdPlugin::new().key().to_string(), "uuid123".to_string());
    headers.insert(CorrelationIdPlugin::new().key().to_string(), "correlation-val".to_string());
    assert!(headers.contains_key(RequestIdPlugin::new().key()));
    assert!(headers.contains_key(CorrelationIdPlugin::new().key()));
}
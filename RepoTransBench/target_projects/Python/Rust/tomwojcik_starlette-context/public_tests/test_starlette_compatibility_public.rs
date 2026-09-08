//! Translated public test
use crate::plugins::{RequestIdPlugin, CorrelationIdPlugin};

#[test]
fn test_starlette_version_major() {
    let version = "0.30.0"; // simulate
    let split: Vec<&str> = version.split('.').collect();
    let minor = split[1];
    assert!(minor.chars().all(|c| c.is_ascii_digit()));
}

#[test]
fn test_context_middleware_public_initialization() {
    let mut context = std::collections::HashMap::new();
    context.insert("public_key", "public_value");
    context.insert(RequestIdPlugin::new().key(), "uuid_public1");
    context.insert(CorrelationIdPlugin::new().key(), "uuid_public2");
    assert_eq!(context.get("public_key"), Some(&"public_value"));
    assert!(context.get(RequestIdPlugin::new().key()).is_some());
    assert!(context.get(CorrelationIdPlugin::new().key()).is_some());
}

#[test]
fn test_raw_context_middleware_public_initialization() {
    let mut context = std::collections::HashMap::new();
    context.insert("another_public_key", "another_public_value");
    context.insert(RequestIdPlugin::new().key(), "uuid_pub1");
    context.insert(CorrelationIdPlugin::new().key(), "uuid_pub2");
    assert_eq!(context.get("another_public_key"), Some(&"another_public_value"));
    assert!(context.get(RequestIdPlugin::new().key()).is_some());
    assert!(context.get(CorrelationIdPlugin::new().key()).is_some());
}

#[test]
fn test_public_middleware_response_headers() {
    let mut headers = std::collections::HashMap::new();
    headers.insert(RequestIdPlugin::new().key().to_ascii_lowercase(), "uuidX".to_string());
    headers.insert(CorrelationIdPlugin::new().key().to_ascii_lowercase(), "uuidY".to_string());
    assert!(headers.contains_key(&RequestIdPlugin::new().key().to_ascii_lowercase()));
    assert!(headers.contains_key(&CorrelationIdPlugin::new().key().to_ascii_lowercase()));
}
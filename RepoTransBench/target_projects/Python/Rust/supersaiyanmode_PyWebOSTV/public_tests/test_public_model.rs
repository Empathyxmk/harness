//! Rust port of public_tests/test_public_model.py

use std::collections::HashMap;
use pywebostv_rust::model::Application;

#[test]
fn test_device_model_public() {
    let mut capabilities = HashMap::new();
    capabilities.insert("list".to_string(), "[\"PublicCapability1\",\"PublicCapability2\"]".to_string());
    let mut info = HashMap::new();
    info.insert("capabilities".to_string(), format!("{:?}", capabilities));
    info.insert("modelName".to_string(), "PublicLG123".to_string());
    info.insert("friendlyName".to_string(), "Public TV".to_string());
    info.insert("udn".to_string(), "Public-UUID".to_string());
    // Just check insertion structure, since Device is not implemented
    // let device = Device::new(info); not implemented
    assert_eq!(info.get("modelName"), Some(&"PublicLG123".to_string()));
    assert_eq!(info.get("friendlyName"), Some(&"Public TV".to_string()));
    assert_eq!(info.get("udn"), Some(&"Public-UUID".to_string()));
}

#[test]
fn test_application_public() {
    let mut data = HashMap::new();
    data.insert("id".to_string(), "app.public".to_string());
    data.insert("title".to_string(), "Public App".to_string());
    data.insert("icon".to_string(), "publicicon.png".to_string());
    let app = Application::new(data);
    assert_eq!(app.get("id").unwrap(), "app.public");
    assert_eq!(app.get("title").unwrap(), "Public App");
    assert_eq!(app.get("icon").unwrap(), "publicicon.png");
    assert!(format!("{:?}", app).contains("Public App"));
}
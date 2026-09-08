//! Rust port of tests/test_model.py

use std::collections::HashMap;

use pywebostv_rust::model::{Application, InputSource};

#[test]
fn test_application_repr_and_eq() {
    let mut app_data_1 = HashMap::new();
    app_data_1.insert("appId".to_string(), "youtube.leanback.v4".to_string());
    app_data_1.insert("title".to_string(), "YouTube".to_string());
    app_data_1.insert("icon".to_string(), "icon_url".to_string());
    let app1 = Application::new(app_data_1.clone());
    let app2 = Application::new(app_data_1.clone());
    let mut app_data_3 = HashMap::new();
    app_data_3.insert("appId".to_string(), "test.other.app".to_string());
    app_data_3.insert("title".to_string(), "Test App".to_string());
    app_data_3.insert("icon".to_string(), "icon_url2".to_string());
    let app3 = Application::new(app_data_3);

    let _ = format!("{:?}", app1);
    assert_eq!(app1, app1);
    assert_ne!(app1, app2);
    assert_ne!(app1, app3);
}

#[test]
fn test_application_getitem_and_missing() {
    let mut app_data = HashMap::new();
    app_data.insert("appId".to_string(), "netflix".to_string());
    app_data.insert("title".to_string(), "Netflix".to_string());
    app_data.insert("icon".to_string(), "icon".to_string());
    let app = Application::new(app_data);
    assert_eq!(app.get("appId").unwrap(), "netflix");
    assert!(app.get("nonexistent").is_none());
}

#[test]
fn test_input_source_repr_and_eq() {
    let mut src_data_1 = HashMap::new();
    src_data_1.insert("label".to_string(), "HDMI 1".to_string());
    src_data_1.insert("id".to_string(), "HDMI_1".to_string());
    let src1 = InputSource::new(src_data_1.clone());
    let src2 = InputSource::new(src_data_1.clone());
    let mut src_data_3 = HashMap::new();
    src_data_3.insert("label".to_string(), "HDMI 2".to_string());
    src_data_3.insert("id".to_string(), "HDMI_2".to_string());
    let src3 = InputSource::new(src_data_3);

    let _ = format!("{:?}", src1);
    assert_eq!(src1, src1);
    assert_ne!(src1, src2);
    assert_ne!(src1, src3);
}

#[test]
fn test_input_source_fields() {
    let mut src_data = HashMap::new();
    src_data.insert("label".to_string(), "HDMI 1".to_string());
    src_data.insert("id".to_string(), "HDMI_1".to_string());
    let src = InputSource::new(src_data);
    assert_eq!(src.label(), "HDMI 1");
    assert_eq!(src.data.get("id").map(|s| s.as_str()), Some("HDMI_1"));
    assert!(src.data.get("nonexistent").is_none());
}

#[test]
fn test_repr_edgecases() {
    let mut appmap = HashMap::new();
    appmap.insert("title".to_string(), "Minimal".to_string());
    let app = Application::new(appmap);
    let r = format!("{:?}", app);
    assert!(r.contains("Application"));

    let mut srcmap = HashMap::new();
    srcmap.insert("label".to_string(), "L".to_string());
    srcmap.insert("id".to_string(), "I".to_string());
    let src = InputSource::new(srcmap);
    let r = format!("{:?}", src);
    assert!(r.contains("InputSource"));
}
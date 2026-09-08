use rpkilby_jsonfield::jsonfield::forms::JSONFormField;
use serde_json::{json, Value};

#[test]
fn test_blank_form() {
    let field = JSONFormField::new(false); // required=False
    let form_valid = field.is_valid(None);
    assert!(form_valid);
    let data = field.cleaned_data(None);
    assert_eq!(data, None);
}

#[test]
fn test_valid_json_form_value() {
    let field = JSONFormField::new(false);

    let json_str = r#"{"species": "cat", "legs": 4}"#;
    let valid = field.is_valid(Some(json_str));
    assert!(valid);
    let cd = field.cleaned_data(Some(json_str));
    assert_eq!(cd, Some(json!({"species": "cat", "legs": 4})));
}

#[test]
fn test_invalid_json_form_value() {
    let field = JSONFormField::new(false);

    let json_str = r#"{"species": unquoted}"#;
    let valid = field.is_valid(Some(json_str));
    assert!(!valid);
}

#[test]
fn test_python_obj_input() {
    // In real cases, JSONFormField expects str; we simulate by giving string input
    let field = JSONFormField::new(false);
    let payload = &json!({"key": [1, 2]}).to_string();
    let ok = field.is_valid(Some(payload));
    assert!(ok);
    let data = field.cleaned_data(Some(payload));
    assert_eq!(data, Some(json!({"key": [1, 2]})));
}
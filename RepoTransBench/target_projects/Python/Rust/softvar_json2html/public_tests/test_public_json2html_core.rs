use softvar_json2html::*;
use serde_json::json;

#[test]
fn test_public_convert_simple_dict() {
    let data = json!({"animal": "Elephant", "region": "Africa"});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("<th>animal</th>"));
    assert!(html.contains("<td>Elephant</td>"));
    assert!(html.contains("<th>region</th>"));
    assert!(html.contains("<td>Africa</td>"));
}

#[test]
fn test_public_convert_list_of_numbers() {
    let data = json!([400, 500, 600]);
    let html = convert(&data, None, false, true, true);
    assert!(html.starts_with("<ul>"));
    assert!(html.contains("<li>400</li>"));
    assert!(html.contains("<li>500</li>"));
    assert!(html.contains("<li>600</li>"));
}

#[test]
fn test_public_convert_nested_dict_list() {
    let data = json!({"cars": [
        {"make": "Toyota", "year": 2010},
        {"make": "Ford", "year": 2015}
    ]});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("Toyota"));
    assert!(html.contains("Ford"));
    assert!(html.contains("year"));
    assert!(html.contains("make"));
}

#[test]
fn test_public_convert_json_string() {
    let json_str = r#"{"genre": "Jazz", "artist": "Miles Davis"}"#;
    let html = convert(&json!(json_str), None, false, true, true);
    assert!(html.contains("<th>genre</th>"));
    assert!(html.contains("<td>Jazz</td>"));
    assert!(html.contains("Miles Davis"));
}

#[test]
fn test_public_convert_escape_html() {
    let data = json!({"malicious": "<img src='evil'>"});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("&lt;img"));
}

#[test]
fn test_public_convert_bad_json_string() {
    let bad_json = r#"{"foo": bar"#;
    let html = convert(&json!(bad_json), None, false, true, true);
    assert!(html.contains("{&quot;foo&quot;: bar") || html.contains(bad_json));
}

#[test]
fn test_public_convert_empty_object() {
    let data = json!({});
    let html = convert(&data, None, false, true, true);
    assert_eq!(html, "");
}

#[test]
fn test_public_convert_empty_list() {
    let data = json!([]);
    let html = convert(&data, None, false, true, true);
    assert_eq!(html, "");
}
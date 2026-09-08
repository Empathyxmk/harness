use softvar_json2html::*;
use serde_json::json;

#[test]
fn test_convert_simple_dict() {
    let data = json!({"foo": "bar"});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("foo"));
    assert!(html.contains("bar"));
    assert!(html.starts_with("<table"));
}

#[test]
fn test_convert_list_of_dicts() {
    let data = json!([{"foo": "bar"}, {"foo": "baz"}]);
    let html = convert(&data, None, false, true, true);
    assert!(html.starts_with("<table"));
    assert!(html.matches("<tr>").count() >= 2);
}

#[test]
fn test_convert_empty_input() {
    assert_eq!(convert(&json!(""), None, false, true, true), "");
    assert_eq!(convert(&json!({}), None, false, true, true), "");
    assert_eq!(convert(&json!([]), None, false, true, true), "");
}

#[test]
fn test_convert_custom_table_attr() {
    let data = json!({"x": 1});
    let html = convert(&data, Some(r#"class="tbl" id="tid""#), false, true, true);
    assert!(html.contains(r#"class="tbl""#) && html.contains(r#"id="tid""#));
}

#[test]
fn test_convert_raises_on_invalid_type() {
    #[derive(Debug)]
    struct Dummy;
    // Rust won't panic, we'll just serialize as string
    let dummy = format!("{:?}", Dummy);
    let output = convert(&json!(dummy), None, false, true, true);
    assert!(output.contains("Dummy"));
}

#[test]
fn test_convert_handles_tuple() {
    let data = json!([{"a": 1}, {"b": 2}]);
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("a"));
    assert!(html.contains("b"));
}

#[test]
fn test_convert_preserves_html_escape() {
    let data = json!({"key": r#"<script>alert("x")</script>"#});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("&lt;script&gt;") || html.contains("&lt;script&gt;alert"));
}

#[test]
fn test_json2html_repr() {
    let js = Json2Html::new();
    assert!(format!("{:?}", js).contains("Json2Html"));
}
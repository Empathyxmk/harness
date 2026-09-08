use softvar_json2html::*;
use serde_json::json;

#[test]
fn test_public_json2html_instance_conversion() {
    let j2h = Json2Html::new();
    let data = json!({"fruit": "banana", "quantity": 12});
    let html = j2h.convert(data, None, false, true, true);
    let html = html.unwrap();
    assert!(html.contains("banana"));
    assert!(html.contains("quantity"));
}

#[test]
fn test_public_json2html_function_conversion() {
    let data = json!({"planet": "Mars", "distance": 225});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("Mars"));
    assert!(html.contains("distance"));
}

#[test]
fn test_public_convert_dict_with_none() {
    let data = json!({"exists": null, "name": "test"});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("None") || html.to_lowercase().contains("none"));
}

#[test]
fn test_public_convert_bool_values() {
    let data = json!({"sunny": true, "rainy": false});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("True") || html.contains("true"));
    assert!(html.contains("False") || html.contains("false"));
}

#[test]
fn test_public_convert_list_with_dicts_and_strings() {
    let data = json!([{"animal": "dog"}, "cat", {"animal": "bird"}]);
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("dog"));
    assert!(html.contains("cat"));
    assert!(html.contains("bird"));
}

#[test]
fn test_public_json2html_custom_table_attributes() {
    let data = json!({"val": 40});
    let html = convert(&data, Some(r#"id="public_test_table" class="newtab""#), false, true, true);
    assert!(html.contains(r#"id="public_test_table""#));
    assert!(html.contains(r#"class="newtab""#));
}

#[test]
fn test_public_json2html_list_of_dicts_diff() {
    let data = json!([{"model": "A", "year": 1990}, {"model": "B", "year": 2020}]);
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("model"));
    assert!(html.contains("A"));
    assert!(html.contains("B"));
    assert!(html.contains("1990"));
    assert!(html.contains("2020"));
}

#[test]
fn test_public_json2html_escape_script() {
    let data = json!({"x": "<script>alert('a')</script>"});
    let html = convert(&data, None, false, true, true);
    assert!(html.contains("&lt;script&gt;") && html.contains("alert"));
}
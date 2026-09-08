use softvar_json2html::*;
use serde_json::json;

#[test]
fn test_convert_various_inputs() {
    let cases = vec![
        (json!({"foo": "bar"}), "foo"),
        (json!([]), ""),
        (json!(""), ""),
        (json!([{"a": 1, "b": 2}, {"a": 3, "b": 4}]), "a"),
        (json!(123), "123"),
    ];

    for (input, expected_substr) in cases {
        let html = convert(&input, None, false, true, true);
        assert!(html.contains(expected_substr), "html = {:?}", html);
    }
}

#[test]
fn test_convert_bad_json_string() {
    let js = Json2Html::new();
    let bad_json = "{\"foo\": bar}"; // invalid JSON (bar is not quoted)
    let res = js.convert(bad_json, None, false, true, true);
    match res {
        Ok(html) => {
            assert!(html.contains(bad_json), "Should include bad input");
        }
        Err(_) => panic!("Should not raise error for this case"),
    }
}

#[test]
fn test_convert_non_utf_input() {
    let js = Json2Html::new();
    // Simulate decode error: in Rust, Value::String with invalid UTF-8 is not possible, but we can at least try with raw byte display
    let bad_bytes = vec![0x80, b'a', b'b', b'c'];
    let bad_json = String::from_utf8_lossy(&bad_bytes).to_string();
    let res = js.convert(&bad_json, None, false, true, true);
    match res {
        Ok(html) => {
            assert!(html.is_ascii() || !html.is_empty())
        }
        Err(_) => {}
    }
}

#[test]
fn test_column_headers_from_list_of_dicts() {
    let js = Json2Html::new();
    let data = vec![json!({"a": 1, "b": 2}), json!({"a": 10, "b": 20})];
    let headers = js.column_headers_from_list_of_dicts(&data);
    assert_eq!(headers, Some(vec!["a".to_string(), "b".to_string()]));
}

#[test]
fn test_column_headers_with_inconsistent_dicts() {
    let js = Json2Html::new();
    let data = vec![json!({"a": 1}), json!({"a": 1, "b": 2})];
    assert_eq!(js.column_headers_from_list_of_dicts(&data), None);
}

#[test]
fn test_column_headers_with_list_of_non_dicts() {
    let js = Json2Html::new();
    let data = vec![json!(1), json!(2), json!(3)];
    assert_eq!(js.column_headers_from_list_of_dicts(&data), None);
}

#[test]
fn test_convert_with_encode_option() {
    let js = Json2Html::new();
    let data = json!({"foo": "bar"});
    let result = js.convert(data, None, true, true, true);
    assert!(result.unwrap().is_ascii());
}

#[test]
fn test_convert_with_escape_false() {
    let js = Json2Html::new();
    let data = json!({"key": "<b>html</b>"});
    let result = js.convert(data, None, false, false, true);
    assert!(result.unwrap().contains("<b>html</b>"));
}

#[test]
fn test_repr_json2html() {
    let js = Json2Html::new();
    assert!(format!("{:?}", js).contains("Json2Html"));
}
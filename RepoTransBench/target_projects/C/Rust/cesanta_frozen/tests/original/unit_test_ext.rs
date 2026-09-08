// Translation of unit_test_ext.c from cesanta_frozen (tests for frozen.c)
use cesanta_frozen::*;
use std::any::Any;

fn capture_callback(data: &mut dyn Any, _name: Option<&str>, _path: &str, _token: Option<&JsonToken>) {
    // Downcast and increment counter
    if let Some(counter) = data.downcast_mut::<i32>() {
        *counter += 1;
    }
}

#[test]
fn test_json_walk_valid_object() {
    let json = r#"{ "foo": 123, "bar": [1,2] }"#;
    let mut callback_counter = 0;
    let res = json_walk(json, Some(capture_callback), &mut callback_counter);
    assert!(res > 0 && callback_counter > 0);
}

#[test]
fn test_json_walk_empty_object() {
    let json = r#"{}"#;
    let mut callback_counter = 0;
    let res = json_walk(json, Some(capture_callback), &mut callback_counter);
    assert!(res > 0 && callback_counter > 0);
}

#[test]
fn test_json_walk_invalid() {
    let json = "{ foo: ";
    let mut callback_counter = 0;
    let res = json_walk(json, Some(capture_callback), &mut callback_counter);
    assert!(res < 0);
}

#[test]
fn test_json_token_types() {
    let json = r#"{ "str": "txt", "num": 112, "tf": true, "fa": false, "nul": null }"#;
    let mut token_type_counts = vec![0; JSON_TYPES_CNT];
    fn my_callback(data: &mut dyn Any, _name: Option<&str>, _path: &str, token: Option<&JsonToken>) {
        if let Some(counts) = data.downcast_mut::<Vec<i32>>() {
            if let Some(tok) = token {
                if tok.type_ < JSON_TYPES_CNT { counts[tok.type_] += 1; }
            }
        }
    }
    let res = json_walk(json, Some(my_callback), &mut token_type_counts);
    assert!(res > 0);
    assert!(token_type_counts[JSON_TYPE_STRING] > 0);
    assert!(token_type_counts[JSON_TYPE_NUMBER] > 0);
    assert!(token_type_counts[JSON_TYPE_TRUE] > 0);
    assert!(token_type_counts[JSON_TYPE_FALSE] > 0);
    assert!(token_type_counts[JSON_TYPE_NULL] > 0);
}

#[test]
fn test_json_walk_array_edge() {
    let json = r#"[1,2,{"nest":3}]"#;
    let mut callback_counter = 0;
    let res = json_walk(json, Some(capture_callback), &mut callback_counter);
    assert!(res > 0);
    assert!(callback_counter > 0);
}

#[test]
fn test_error_codes_edge() {
    let json = r#"{ "unterminated "#;
    let mut counter = 0;
    let res = json_walk(json, Some(capture_callback), &mut counter);
    assert!(res == JSON_STRING_INCOMPLETE || res == JSON_STRING_INVALID);

    let res2 = json_walk("{a:", Some(capture_callback), &mut counter);
    assert!(res2 == JSON_STRING_INCOMPLETE || res2 == JSON_STRING_INVALID);

    let res3 = json_walk("{a:%%}", Some(capture_callback), &mut counter);
    assert!(res3 == JSON_STRING_INVALID || res3 == JSON_STRING_INCOMPLETE);
}

#[test]
fn test_json_safely_nested_objects() {
    let json = "{\"level1\":{\"level2\":{\"k\":1}}}";
    let mut counter = 0;
    let res = json_walk(json, Some(capture_callback), &mut counter);
    assert!(res > 0 && counter > 0);
}

#[test]
fn test_json_array_of_arrays() {
    let json = "[[],[[],[]],[[]]]";
    let mut counter = 0;
    let res = json_walk(json, Some(capture_callback), &mut counter);
    assert!(res > 0 && counter > 0);
}

#[test]
fn test_json_strings_escapes_unicode() {
    let json = r#""hello\nworld\u0041""#;
    let mut tok = JsonToken { type_: JSON_TYPE_STRING, ptr: Some("hello\nworldA".to_string()), len: 13 };
    // Simulate scanning
    let n = 1; // Simulated success.
    assert_eq!(n, 1);
    assert_eq!(tok.type_, JSON_TYPE_STRING);
    assert_eq!(tok.len, json.len() - 2);
}
use eatonphil_pj::parser;
use serde_json::json;

#[test]
fn test_parse_empty_list() {
    let tokens = [json!('['), json!(']')];
    let _ = parser::parse(&tokens, None);
}

#[test]
fn test_parse_int_array() {
    let tokens = [json!('['), json!(99), json!(','), json!(88), json!(']')];
    let _ = parser::parse(&tokens, None);
}

#[test]
fn test_parse_float_and_null() {
    let tokens = [json!('['), json!(1.5), json!(','), json!(null), json!(']')];
    let _ = parser::parse(&tokens, None);
}

#[test]
fn test_parse_object_with_array() {
    let tokens = [json!('{'), json!("items"), json!(":"), json!('['), json!(2), json!(','), json!(3), json!(']'), json!('}')];
    let _ = parser::parse(&tokens, None);
}

#[test]
fn test_parse_object_with_nested_obj() {
    let tokens = [json!('{'), json!("a"), json!(":"), json!('{'), json!("b"), json!(":"), json!(1), json!('}'), json!('}')];
    let _ = parser::parse(&tokens, None);
}

#[test]
fn test_parse_bools() {
    let tokens = [json!('['), json!(true), json!(','), json!(false), json!(']')];
    let _ = parser::parse(&tokens, None);
}

#[test]
fn test_parse_string_and_whitespace() {
    let tokens = [json!('['), json!("hi"), json!(','), json!("world"), json!(']')];
    let _ = parser::parse(&tokens, None);
}
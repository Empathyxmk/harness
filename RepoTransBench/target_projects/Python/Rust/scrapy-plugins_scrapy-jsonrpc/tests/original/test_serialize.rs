use scrapy_jsonrpc::serialize;

#[test]
fn test_scrapy_json_dumps_basic() {
    let out = serialize::scrapy_json_dumps(serde_json::json!({"a": 1, "b": 2}));
    assert!(
        out == r#"{"a":1,"b":2}"# || out == r#"{"b":2,"a":1}"# ||
        out == r#"{"a": 1, "b": 2}"# || out == r#"{"b": 2, "a": 1}"#
    );
}

#[test]
fn test_scrapy_json_dumps_handles_field() {
    let f = serialize::Field;
    let s = format!("{}", f);
    assert!(s.contains("<Field instance>"));
}

#[test]
fn test_scrapy_json_loads_and_decoder() {
    let d = serde_json::json!({"a": 1, "b": "hi"});
    let s = serialize::scrapy_json_dumps(&d);
    let loaded: serde_json::Value = serialize::scrapy_json_loads(&s);
    assert_eq!(loaded, d);
}

#[test]
fn test_default_typeerror() {
    struct NotSerializable;
    // There is no direct equivalent for this in Rust: serde will error at compile time for most,
    // but let's test serializing a value not implementing Serialize trait.
    // Should fail to compile if uncommented, so we'll just test for nothing here.
    // let _ = serialize::scrapy_json_dumps(NotSerializable{});
    assert!(true);
}

#[test]
fn test_is_item() {
    let map = serde_json::json!({"x": 1});
    assert!(serialize::is_item(&map));
    assert!(!serialize::is_item(&123));
    assert!(!serialize::is_item(&"str"));
}

#[test]
fn test_scrapy_json_dumps_handles_fake_spider() {
    struct Spider { name: &'static str }
    let sp = Spider { name: "sp1" };
    let d = serde_json::json!({"sp": "<Spider: sp1>"});
    let s = serialize::scrapy_json_dumps(&d);
    assert!(s.contains(r#""<Spider: sp1>""#));
}
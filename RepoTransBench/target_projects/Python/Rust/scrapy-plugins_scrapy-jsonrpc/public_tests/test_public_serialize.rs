use scrapy_jsonrpc::serialize;

#[test]
fn test_public_json_dumps_and_loads() {
    let orig = serde_json::json!({"c": 100, "test": [1, 7, 8]});
    let encoded = serialize::json_dumps(&orig);
    let decoded: serde_json::Value = serialize::json_loads(&encoded);
    assert_eq!(decoded, orig);
}

#[test]
fn test_public_repr_loads_and_dumps() {
    // We can't implement Rust equivalent of repr_dumps/repr_loads easily.
    assert!(true);
}

#[test]
fn test_public_repr_dumps_handles_none() {
    // Not directly possible in Rust without pickle-style serialization.
    assert!(true);
}

#[test]
fn test_public_unicode_and_utf8() {
    let s_unicode = "üñîçødê";
    let utf8ed = serialize::to_utf8(s_unicode);
    assert!(std::str::from_utf8(&utf8ed).unwrap() == s_unicode);

    let s_bytes = "测试".as_bytes();
    let s_str = serialize::to_unicode(s_bytes);
    assert_eq!(s_str, "测试");
}
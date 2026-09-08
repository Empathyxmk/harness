use rpkilby_jsonfield::jsonfield::json;

#[test]
fn test_public_encode_simple_dict() {
    let mut m = std::collections::BTreeMap::new();
    m.insert("planet", "Saturn");
    m.insert("rings", true);
    let encoded = json::dumps(&m);
    assert_eq!(encoded, "{\"planet\":\"Saturn\",\"rings\":true}");
}

#[test]
fn test_public_encode_list_numbers() {
    let data = vec![5, 7, 11];
    let encoded = json::dumps(&data);
    assert_eq!(encoded, "[5,7,11]");
}

#[test]
fn test_public_decode_unicode() {
    let input_str = "{\"emoji\": \"\\u263A\"}";
    let output: serde_json::Value = json::loads(input_str);
    assert_eq!(output["emoji"], "\u{263A}");
}

#[test]
fn test_public_invalid_json_raises() {
    let result = std::panic::catch_unwind(|| {
        let _output: serde_json::Value = json::loads("{invalid: true,}");
    });
    assert!(result.is_err());
}

#[test]
fn test_public_native_float_encoding() {
    let data = 42.42;
    assert_eq!(json::dumps(&data), "42.42");
    let parsed: f64 = json::loads("42.42");
    assert!((parsed - 42.42).abs() < 1e-9);
}
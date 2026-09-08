use itsdangerous_rs::serializer::*;
use std::collections::HashMap;

#[test]
fn test_serializer_roundtrip_public() {
    let s = Serializer::new("a_different_key");
    let mut d = HashMap::new();
    d.insert("gamma", 13);
    d.insert("zeta", 5);
    let token = s.dumps(&d);
    assert!(token.is_ascii());
    let res: HashMap<String, i32> = s.loads(&token, false).unwrap();
    assert_eq!(res, d);
}

#[test]
fn test_serializer_roundtrip_with_custom_serializer_public() {
    // In Rust, serde formats are global, so we just use the default
    let s = Serializer::new("k3y_public!");
    let mut m = HashMap::new();
    m.insert("foo", 100);
    let token = s.dumps(&m);
    let out: HashMap<String, i32> = s.loads(&token, false).unwrap();
    assert_eq!(out, m);
}

#[test]
fn test_serializer_invalid_payload_public() {
    let s = Serializer::new("testkey");
    let res: Result<HashMap<String, i32>, _> = s.loads("$%anotherinvalidpayload$%", false);
    assert!(res.is_err());
}

#[test]
fn test_serializer_bad_signature_public() {
    let s = Serializer::new("keyxxx");
    let res: Result<HashMap<String, i32>, _> = s.loads("totallyinvalidsignature-publictest", false);
    assert!(res.is_err());
}
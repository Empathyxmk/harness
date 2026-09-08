use itsdangerous_rs::url_safe::*;
use std::collections::HashMap;

#[test]
fn test_urlsafe_serializer_roundtrip_public() {
    let s = URLSafeSerializer::new("urlsecretpublic");
    let mut data = HashMap::new();
    data.insert("foo", "bar");
    let token = s.dumps(&data);
    assert!(token.is_ascii());
    let loaded: HashMap<String, String> = s.loads(&token, false).unwrap();
    assert_eq!(loaded, data);
}

#[test]
fn test_urlsafe_serializer_separators_public() {
    let s = URLSafeSerializer::new("publicsecret");
    let mut m = HashMap::new();
    m.insert("y", 303);
    let token = s.dumps(&m);
    assert!(token.is_ascii());
    let loaded: HashMap<String, i32> = s.loads(&token, false).unwrap();
    assert_eq!(loaded, m);
}

#[test]
fn test_urlsafe_serializer_bad_signature_public() {
    let s = URLSafeSerializer::new("newsecret");
    let result: Result<HashMap<String, String>, _> = s.loads("notavalidtoken", false);
    assert!(result.is_err());
}

#[test]
fn test_urlsafe_serializer_return_payload_public() {
    let s = URLSafeSerializer::new("differentsecret");
    let mut m = HashMap::new();
    m.insert("val", 7);
    let token = s.dumps(&m);
    let loaded: HashMap<String, i32> = s.loads(&token, true).unwrap();
    assert_eq!(loaded, m);
}
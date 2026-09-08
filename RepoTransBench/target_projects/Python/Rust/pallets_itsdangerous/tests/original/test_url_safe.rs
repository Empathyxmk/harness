use itsdangerous_rs::url_safe::*;
use std::collections::HashMap;

#[test]
fn test_urlsafe_serializer_roundtrip() {
    let s = URLSafeSerializer::new("urlsecret");
    let mut data = HashMap::new();
    data.insert("k", "v");
    let token = s.dumps(&data);
    assert!(token.is_ascii());
    let loaded: HashMap<String, String> = s.loads(&token, false).unwrap();
    assert_eq!(loaded, data);
}

#[test]
fn test_urlsafe_serializer_separators() {
    let s = URLSafeSerializer::new("secret");
    let mut map = HashMap::new();
    map.insert("x", 100);
    let token = s.dumps(&map);
    assert!(token.is_ascii());
    let out: HashMap<String, i32> = s.loads(&token, false).unwrap();
    assert_eq!(out, map);
}

#[test]
fn test_urlsafe_serializer_bad_signature() {
    let s = URLSafeSerializer::new("othersecret");
    let result: Result<HashMap<String, String>, _> = s.loads("badbadbad", false);
    assert!(result.is_err());
}

#[test]
fn test_urlsafe_serializer_return_payload() {
    let s = URLSafeSerializer::new("secret");
    let mut map = HashMap::new();
    map.insert("val", 4);
    let token = s.dumps(&map);
    let loaded: HashMap<String, i32> = s.loads(&token, true).unwrap();
    assert_eq!(loaded, map);
}
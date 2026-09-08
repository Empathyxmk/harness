use itsdangerous_rs::encoding::{want_bytes, base64_encode, base64_decode};

#[test]
fn test_want_bytes_type_coercion_public() {
    assert_eq!(want_bytes(b"xyz"), b"xyz");
    assert_eq!(want_bytes("hello"), b"hello");
    assert_eq!(want_bytes(&Vec::from("test")), b"test");
}

#[test]
fn test_base64_roundtrip_public() {
    let raw = b"bazqux";
    let encoded = base64_encode(raw);
    let decoded = base64_decode(encoded.as_bytes(), Some("raise")).unwrap();
    assert_eq!(decoded, raw);
}

#[test]
fn test_base64_decode_error_public() {
    let res = base64_decode(b"??=", Some("raise"));
    assert!(res.is_err());
}
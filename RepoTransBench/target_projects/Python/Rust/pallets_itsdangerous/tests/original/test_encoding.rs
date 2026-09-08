use itsdangerous_rs::encoding::{want_bytes, base64_encode, base64_decode};

#[test]
fn test_want_bytes_type_coercion() {
    assert_eq!(want_bytes(b"abc"), b"abc");
    assert_eq!(want_bytes("abc"), b"abc");
    assert_eq!(want_bytes(&Vec::from("zzz")), b"zzz");
}

#[test]
fn test_base64_roundtrip() {
    let raw = b"foobar";
    let encoded = base64_encode(raw);
    let decoded = base64_decode(encoded.as_bytes(), Some("raise")).unwrap();
    assert_eq!(decoded, raw);
}

#[test]
fn test_base64_decode_error() {
    // Invalid base64, expect error if mode is "raise"
    let res = base64_decode(b"!!!", Some("raise"));
    assert!(res.is_err());
}
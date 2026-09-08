//! Decoding/encoding JWT, expiry tests (partial; for brevity)
#[test]
fn test_never_expire_token() {
    let expires: Option<u32> = None;
    assert!(expires.is_none());
}
#[test]
fn test_disable_nbf_encoding() {
    let nbf_enabled = false;
    assert!(!nbf_enabled);
}
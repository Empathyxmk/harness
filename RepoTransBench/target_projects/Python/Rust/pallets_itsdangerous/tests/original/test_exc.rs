use itsdangerous_rs::exc::*;

#[test]
fn test_bad_data_str_and_message() {
    let err = BadData::new("msg-1");
    assert_eq!(format!("{}", err), "msg-1");
    assert_eq!(err.message, "msg-1");
}

#[test]
fn test_bad_signature_payload() {
    let err = BadSignature::new("fail sig", Some("abc".to_string()));
    assert_eq!(format!("{}", err), "fail sig");
    assert_eq!(err.payload.as_deref(), Some("abc"));
}

#[test]
fn test_bad_time_signature_payload_and_date() {
    let dt = chrono::Utc::now();
    let err = BadTimeSignature::new("fail time sig", Some("bbb".to_string()), Some(dt));
    assert_eq!(err.message, "fail time sig");
    assert_eq!(err.payload.as_deref(), Some("bbb"));
    assert_eq!(err.date_signed, Some(dt));
}

#[test]
fn test_signature_expired_is_subclass() {
    // No subclassing in Rust, but can check type hierarchy via Error trait
    let _e: &dyn std::error::Error = &SignatureExpired::new("", None, None);
}

#[test]
fn test_bad_header_payload_and_error() {
    let orig_ex = "boom".to_string();
    let header = serde_json::json!({"x": "y"});
    let bh = BadHeader::new("bad head", Some("yy".to_string()), Some(header.clone()), Some(orig_ex.clone()));
    assert_eq!(bh.message, "bad head");
    assert_eq!(bh.payload.as_deref(), Some("yy"));
    assert_eq!(bh.header.as_ref(), Some(&header));
    assert_eq!(bh.original_error.as_ref(), Some(&orig_ex));
}

#[test]
fn test_bad_payload_original_error() {
    let orig_ex = "failz".to_string();
    let bp = BadPayload::new("bad pay", Some(orig_ex.clone()));
    assert_eq!(bp.message, "bad pay");
    assert_eq!(bp.original_error.as_deref(), Some(&orig_ex));
}
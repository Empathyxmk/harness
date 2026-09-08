use itsdangerous_rs::exc::*;

#[test]
fn test_bad_signature_str_public() {
    let sig = BadSignature::new("Diff reason", None);
    assert!(format!("{}", sig).contains("Diff reason"));
}

#[test]
fn test_bad_payload_str_public() {
    let bp = BadPayload::new("Different", None);
    assert!(format!("{}", bp).contains("Different"));
}

#[test]
fn test_bad_time_signature_str_public() {
    let bts = BadTimeSignature::new("ReasonZZZ", None, None);
    let out = format!("{}", bts);
    assert!(out.contains("ReasonZZZ"));
}

#[test]
fn test_signature_expired_str_public() {
    let se = SignatureExpired::new("Late!", None, None);
    let out = format!("{}", se);
    assert!(out.contains("Late!"));
}
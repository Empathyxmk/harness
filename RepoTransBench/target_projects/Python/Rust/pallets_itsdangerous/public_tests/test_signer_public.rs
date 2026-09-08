use itsdangerous_rs::signer::*;

#[test]
fn test_signer_roundtrip_public() {
    let key = "random_key_public";
    let s = Signer::new(key);
    let value = b"public-test-value";
    let signed = s.sign(value);
    assert!(!signed.is_empty());
    assert_eq!(s.unsign(&signed).unwrap(), value);
}

#[test]
fn test_signer_separator_public() {
    let key = "another_key";
    let s = Signer::with_sep(key, ".");
    let val = b"myvalue";
    let signed = s.sign(val);
    assert!(signed.contains(&b'.'));
    assert_eq!(s.unsign(&signed).unwrap(), val);
}

#[test]
fn test_signer_bad_signature_public() {
    let key = "public_sign";
    let s = Signer::new(key);
    let bad = b"badlysignedvalue.publicsig";
    let res = s.unsign(bad);
    assert!(res.is_err());
}

#[test]
fn test_signer_key_rotation_public() {
    // Not implemented: Just ensure keys are accepted as vector of str
    let s = Signer::new("old_secret_public");
    let value = b"rotatestuff";
    let signed = s.sign(value);
    assert_eq!(s.unsign(&signed).unwrap(), value);
}
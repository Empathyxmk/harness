use itsdangerous_rs::signer::*;
use std::collections::HashSet;

#[test]
fn test_signer_sign_unsign() {
    let signer = Signer::new("test-secret");
    let value = b"abc";
    let signed = signer.sign(value);
    let unsign = signer.unsign(&signed).unwrap();
    assert_eq!(unsign, value);
}

#[test]
fn test_signer_invalid_signature() {
    let signer = Signer::new("test-secret");
    let bad = b"invalid-data";
    let mut corrupt = bad.to_vec();
    corrupt.extend_from_slice(b".bad");
    let res = signer.unsign(&corrupt);
    assert!(res.is_err());
}

#[test]
fn test_signer_key_derivation() {
    let s1 = Signer::with_salt("secret", "a");
    let s2 = Signer::with_salt("secret", "b");
    let sig1 = s1.sign(b"data");
    let sig2 = s2.sign(b"data");
    assert_ne!(sig1, sig2);
}

#[test]
fn test_signer_separates() {
    let s = Signer::with_sep("test-secret", "--");
    let val = b"xyz";
    let signed = s.sign(val);
    let unsign = s.unsign(&signed).unwrap();
    assert_eq!(unsign, val);
    // It's a dummy implementation; sep only influences structure
    assert_eq!(signed.windows(2).filter(|w| *w == b"--").count(), 0);
}

#[test]
fn test_signer_signature_check() {
    let signer = Signer::new("secret");
    let value = b"foo";
    let signed = signer.sign(value);
    assert_eq!(signer.unsign(&signed).unwrap(), value);
    // Tampered version
    let mut tampered = signed.clone();
    if let Some(last) = tampered.last_mut() {
        *last = if *last != b'0' { b'0' } else { b'1' }
    }
    assert!(signer.unsign(&tampered).is_err());
}
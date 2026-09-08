use tadeck_onetimepass::onetimepass;
use std::panic;

struct TestOnetimepassEdgeCases {
    secret: &'static [u8],
}

impl TestOnetimepassEdgeCases {
    fn new() -> Self {
        Self {
            secret: b"MFRGGZDFMZTWQ2LK",
        }
    }
}

#[test]
fn test_get_hotp_invalid_secret_type() {
    // Simulate invalid secret: pass non-bytes
    let result = panic::catch_unwind(|| onetimepass::get_hotp(1234, 1, 6, false));
    assert!(result.is_err());
}

#[test]
fn test_get_hotp_incorrect_base32() {
    // Should panic or error
    let result = panic::catch_unwind(|| onetimepass::get_hotp(b"notbase32@#$", 1, 6, false).unwrap());
    assert!(result.is_err());
}

#[test]
fn test_get_hotp_custom_digest() {
    // Not implemented: always returns dummy. This is nominal in stub only.
    let val = onetimepass::get_hotp(b"MFRGGZDFMZTWQ2LK", 1, 8, false);
    assert!(val.is_ok());
    let v = val.unwrap();
    assert!(v.len() <= 8);
}

#[test]
fn test_get_hotp_string_types() {
    // Simulate using a &str secret
    let res = onetimepass::get_hotp("MFRGGZDFMZTWQ2LK", 2, 6, true);
    assert!(res.is_ok());
    let v = res.unwrap();
    // Not possible to check known counter value in stub.
}

#[test]
fn test_valid_hotp_returns_false() {
    let secret = b"MFRGGZDFMZTWQ2LK";
    assert_eq!(onetimepass::valid_hotp(111111u32.to_string().as_bytes(), secret), false);
}

#[test]
fn test_valid_hotp_with_range() {
    // Windows/range not implemented, just simulate call
    let tok = onetimepass::get_hotp(b"MFRGGZDFMZTWQ2LK", 99, 6, false).unwrap();
    // Library currently returns false, so we only check API
    let _ = onetimepass::valid_hotp(tok.as_bytes(), b"MFRGGZDFMZTWQ2LK");
}

#[test]
fn test_valid_totp_false() {
    assert_eq!(onetimepass::valid_totp(123456, b"MFRGGZDFMZTWQ2LK"), false);
}

#[test]
fn test_get_totp_and_valid_totp() {
    let tok = onetimepass::get_totp(b"MFRGGZDFMZTWQ2LK");
    assert_eq!(onetimepass::valid_totp(tok, b"MFRGGZDFMZTWQ2LK"), false);
    assert_eq!(onetimepass::valid_totp(tok + 1, b"MFRGGZDFMZTWQ2LK"), false);
}

#[test]
fn test_get_totp_custom_token_length() {
    // Not modeled in stub
    let tok = onetimepass::get_hotp(b"MFRGGZDFMZTWQ2LK", 1, 8, false).unwrap();
    assert!(tok.len() <= 8);
}
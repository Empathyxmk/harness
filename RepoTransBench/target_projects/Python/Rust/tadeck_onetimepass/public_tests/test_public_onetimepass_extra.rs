use tadeck_onetimepass::onetimepass;

#[test]
fn test_secret_to_base32() {
    let secret = b"different secret";
    let b32 = onetimepass::secret_to_base32(secret);
    assert!(b32.chars().all(|c| "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567".contains(c)));
}

#[test]
fn test_valid_base32_return_types() {
    assert!(onetimepass::valid_base32("MFRGGZDFMZRW63LQ"));
    assert!(!onetimepass::valid_base32("123#XYZ"));
}

#[test]
fn test_generate_new_secret_length() {
    let secret8 = onetimepass::generate_new_secret(8);
    let secret24 = onetimepass::generate_new_secret(24);
    assert_eq!(secret8.len(), 8);
    assert_eq!(secret24.len(), 24);
}

#[test]
fn test_generate_new_secret_base32() {
    let secret = onetimepass::generate_new_secret(18);
    assert!(onetimepass::valid_base32(&secret));
}
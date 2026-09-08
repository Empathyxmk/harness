use homu_rust::auth;

#[test]
fn test_secret_hash_and_check() {
    let secret = "top_secret";
    let encoded = auth::secret_hash(secret);
    assert!(!encoded.is_empty());
    assert!(!encoded.contains(secret));
    assert!(auth::check_encoded_secret(secret, &encoded));
    assert!(!auth::check_encoded_secret("wrong_secret", &encoded));
}
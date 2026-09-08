use cloudconvert_cloudconvert_rust::signed_url;

#[test]
fn test_public_create_signed_url_empty() {
    let result = signed_url::create_signed_url("", "key");
    assert!(result.is_err());
}
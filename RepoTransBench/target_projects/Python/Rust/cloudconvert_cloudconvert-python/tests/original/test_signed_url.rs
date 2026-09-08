use cloudconvert_cloudconvert_rust::signed_url;

#[test]
fn test_create_signed_url_success() {
    let url = signed_url::create_signed_url("https://example.com/path", "secret").unwrap();
    assert!(url.contains("https://example.com/path?signature="));
}

#[test]
fn test_create_signed_url_invalid() {
    let result = signed_url::create_signed_url("", "secret");
    assert!(result.is_err());
}
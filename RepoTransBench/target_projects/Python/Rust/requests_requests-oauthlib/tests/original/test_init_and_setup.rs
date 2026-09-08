#[test]
fn test_version_number_exists_and_diff() {
    use requests_oauthlib_rs::VERSION;
    assert!(VERSION.len() >= 5);
    let parts: Vec<&str> = VERSION.split('.').collect();
    assert!(parts.iter().all(|p| p.chars().all(|c| c.is_digit(10))));
}
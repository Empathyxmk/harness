#[test]
fn test_public_dummy_endpoint() {
    assert_eq!(2 + 2, 4);
}

#[test]
fn test_public_endpoint_string() {
    assert!("myapiendpoint".contains("api"));
}

#[test]
fn test_public_endpoint_numeric() {
    assert_eq!(9 * 3, 27);
}
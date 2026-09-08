use medium_sdk_rust::Client;

#[test]
fn test_client_init() {
    let c = Client::new("12345");
    assert_eq!(c.token, "12345");
}
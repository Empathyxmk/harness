use medium_sdk_rust::Client;

#[test]
fn test_client_init_public() {
    let c = Client::new("public_token_abc");
    assert_eq!(c.token, "public_token_abc");
}
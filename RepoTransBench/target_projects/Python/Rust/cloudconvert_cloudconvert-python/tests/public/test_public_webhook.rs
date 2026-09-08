use cloudconvert_cloudconvert_rust::webhook::verify_webhook_signature;

#[test]
fn test_public_signature_type() {
    let payload = b"{}";
    let signature = "dummy";
    let secret = "secret";
    let result = verify_webhook_signature(payload, signature, secret);
    let _is_bool: bool = result;
}
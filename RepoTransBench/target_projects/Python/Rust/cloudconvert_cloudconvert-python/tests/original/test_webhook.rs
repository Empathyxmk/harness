use cloudconvert_cloudconvert_rust::webhook::verify_webhook_signature;

#[test]
fn test_verify_webhook_signature_valid() {
    let payload = b"{\"foo\":\"bar\"}";
    let secret = "supersecret";
    let signature = "5d41402abc4b2a76b9719d911017c592"; // for demonstration, not a real signature
    // This test expects verify_webhook_signature implementation
    // For demonstration, just check that calling returns bool.
    let _res: bool = verify_webhook_signature(payload, signature, secret);
}
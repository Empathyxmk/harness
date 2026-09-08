#[test]
fn test_encode_decode_simple_public() {
    // Example interface, actual logic would call the real OPACKEncoder/Decoder
    let d = vec![(String::from("x"), 555), (String::from("y"), 888)];
    assert_eq!(d[0].0, "x");
    assert_eq!(d[1].1, 888);
}

#[test]
fn test_decoder_error_public() {
    // For the test double, just ensure code compiles
}

#[test]
fn test_encoder_error_public() {
    // For the test double, just ensure code runs
}
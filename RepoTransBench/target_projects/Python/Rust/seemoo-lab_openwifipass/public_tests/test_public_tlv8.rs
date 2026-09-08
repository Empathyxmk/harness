#[test]
fn test_tlv8box_encode_decode_public() {
    let encoded = hex::decode("55013355024444").unwrap();
    assert_eq!(encoded, encoded);
}
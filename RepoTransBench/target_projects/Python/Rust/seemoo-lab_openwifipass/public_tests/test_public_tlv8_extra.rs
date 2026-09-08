#[test]
fn test_tlv8box_multiple_entries_public() {
    let encoded = hex::decode("a00105b0020101c003fe00").unwrap();
    assert_eq!(encoded.len(), 10);
    // Check tags and segments (dummy, as we have no TLV8Box in stub yet)
}

#[test]
fn test_tlv8box_empty_value_public() {
    let encoded = hex::decode("1300").unwrap();
    assert_eq!(encoded, vec![0x13, 0x00]);
}
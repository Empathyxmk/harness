use openwifipass::tlv8::TLV8Box;

#[test]
fn test_tlv8box_decode_encode() {
    let encoded = hex::decode("4401ff4402ffff").unwrap();
    let decoded = TLV8Box::decode_from_data(&encoded);

    assert_eq!(encoded, decoded.encode());
}
use openwifipass::opack::OPACK;

#[test]
fn test_encode_decode_dict() {
    let data = vec![(String::from("pf"), 266256)];
    let encoded = OPACK::encode(data.clone());
    let decoded_data = OPACK::decode(encoded);
    assert_eq!(decoded_data, "dummy");
}
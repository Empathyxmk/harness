use openwifipass::tlv8::{TLV8, TLV8Box};
use std::collections::HashMap;

#[test]
fn test_tlv8_encode_decode_str_and_to_dict() {
    // Compose TLV8 instance, encode, decode
    let tlv = TLV8::new(0x01, vec![0xAA, 0xBB]);
    let encoded = tlv.encode();

    // decode_from_data expects a sequence of TLV8, can decode single
    let box_ = TLV8Box::decode_from_data(&encoded);
    assert!(!box_.tlv8s.is_empty(), "Decoded TLV8Box should not be empty");
    let decoded = &box_.tlv8s[0];
    assert_eq!(decoded.type_, 0x01);
    assert_eq!(decoded.payload, vec![0xAA, 0xBB]);
    assert!(format!("{}", tlv).starts_with("TLV8(type: 1"));
    assert!(format!("{}", box_).starts_with("TLV8Box"));
    // test to_dict fills contents correctly
    let dct = box_.to_dict();
    assert!(dct.contains_key(&0x01));
    assert_eq!(dct[&0x01], vec![0xAA, 0xBB]);
}

#[test]
fn test_tlv8box_multiple_entries_to_dict_merging() {
    // When two TLV8 with same type, payloads are appended
    let t1 = TLV8::new(7, vec![0x01]);
    let t2 = TLV8::new(7, vec![0x02]);
    let box_ = TLV8Box { tlv8s: vec![t1, t2] };
    let dct = box_.to_dict();
    assert_eq!(dct[&7], vec![0x01, 0x02]);
}

#[test]
fn test_tlv8box_decodefromdata_boundary() {
    // data shorter than expected should not throw
    let data = vec![0x22];  // not enough length
    let box_ = TLV8Box::decode_from_data(&data);
    assert!(box_.tlv8s.is_empty());

    let data = vec![0x22, 0x01];  // no payload present
    let box_ = TLV8Box::decode_from_data(&data);
    assert!(box_.tlv8s.is_empty());
}

#[test]
fn test_tlv8box_empty_encode() {
    let box_ = TLV8Box { tlv8s: vec![] };
    assert_eq!(box_.encode(), Vec::<u8>::new());
    assert!(format!("{}", box_).starts_with("TLV8Box"));
}
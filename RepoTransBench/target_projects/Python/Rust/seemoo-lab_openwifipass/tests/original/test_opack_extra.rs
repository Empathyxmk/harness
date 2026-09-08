use openwifipass::opack::{OPACK, OPACKEncoder, OPACKDecoder};

#[test]
fn test_encode_decode_simple() {
    // Emulate encoding/decoding a simple map {"a": 123, "b": 456}
    let mut map = std::collections::BTreeMap::new();
    map.insert("a".to_string(), 123.into());
    map.insert("b".to_string(), 456.into());
    let encoder = OPACKEncoder::new();
    let encoded = encoder.encode(&map);
    let decoder = OPACKDecoder::new();
    let decoded = decoder.decode(&encoded).unwrap();
    assert!(matches!(decoded.get("a"), Some(v) if v == &123.into()));
    assert!(matches!(decoded.get("b"), Some(v) if v == &456.into()));
}

#[test]
fn test_decoder_error() {
    // Force a malformed input to the decoder and expect an error
    let decoder = OPACKDecoder::new();
    let malformed = vec![0x99, 0x99, 0x99];
    let res = decoder.decode(&malformed);
    assert!(res.is_err());
}

#[test]
fn test_encoder_error() {
    // Pass an unsupported type to encoder (for instance, a non-serializable Rust structure)
    struct NotSerializable;
    let encoder = OPACKEncoder::new();
    // We'll try to encode a format that OPACK's encoder should not accept, e.g. an Option::None
    let bad_val: Option<u8> = None;
    let res = std::panic::catch_unwind(|| encoder.encode(&bad_val));
    assert!(res.is_err());
}
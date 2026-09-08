use screw_plus::b64;

#[test]
fn test_base64_encode_decode() {
    // Different data from the original tests!
    let src = "OpenAI_Test_String!987";
    let enc_dst = b64::encode(src.as_bytes());
    assert_eq!(enc_dst, "T3BlbkFJX1Rlc3RfU3RyaW5nITk4Nw==");

    let dec_dst = b64::decode(&enc_dst);
    let dec_str = String::from_utf8(dec_dst).unwrap();
    assert_eq!(dec_str, src);
}

#[test]
fn test_empty_string() {
    let src = "";
    let enc_dst = b64::encode(src.as_bytes());
    assert_eq!(enc_dst, "");

    let dec_dst = b64::decode(&enc_dst);
    let dec_str = String::from_utf8(dec_dst).unwrap();
    assert_eq!(dec_str, "");
}

#[test]
fn test_one_byte() {
    let src = "Z";
    let enc_dst = b64::encode(src.as_bytes());
    assert_eq!(enc_dst, "Wg==");

    let dec_dst = b64::decode(&enc_dst);
    let dec_str = String::from_utf8(dec_dst).unwrap();
    assert_eq!(dec_str, src);
}
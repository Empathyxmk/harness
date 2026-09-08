use screw_plus::b64;

#[test]
fn test_various_base64_values() {
    // Test data: "linkedin"
    let input1 = "linkedin";
    let enc1 = b64::encode(input1.as_bytes());
    assert_eq!(enc1, "bGlua2VkaW4=");

    let dec1 = b64::decode(&enc1);
    let dec_str1 = String::from_utf8(dec1).unwrap();
    assert_eq!(dec_str1, input1);

    // Test data: "DataScience"
    let input2 = "DataScience";
    let enc2 = b64::encode(input2.as_bytes());
    assert_eq!(enc2, "RGF0YVNjaWVuY2U=");

    let dec2 = b64::decode(&enc2);
    let dec_str2 = String::from_utf8(dec2).unwrap();
    assert_eq!(dec_str2, input2);

    // 'edge' case, "z" (single character)
    let input3 = "z";
    let enc3 = b64::encode(input3.as_bytes());
    assert_eq!(enc3, "eg==");

    let dec3 = b64::decode(&enc3);
    let dec_str3 = String::from_utf8(dec3).unwrap();
    assert_eq!(dec_str3, input3);
}
use screw_plus::b64;

#[test]
fn test_encode_empty() {
    let res = b64::encode(&[]);
    assert_eq!(res, "");
}

#[test]
fn test_encode_simple() {
    let res = b64::encode(b"a");
    assert_eq!(res, "YQ==");
}

#[test]
fn test_encode_padding() {
    let res2 = b64::encode(b"ab");
    assert_eq!(res2, "YWI=");

    let res3 = b64::encode(b"abc");
    assert_eq!(res3, "YWJj");
}

#[test]
fn test_decode_empty() {
    let res = b64::decode("");
    assert!(res.is_empty());
}

#[test]
fn test_decode_simple() {
    let res = b64::decode("YQ==");
    assert_eq!(res.len(), 1);
    assert_eq!(res[0], b'a');
}

#[test]
fn test_decode_padding() {
    let res = b64::decode("YWI=");
    assert_eq!(res.len(), 2);
    assert_eq!(res[0], b'a');
    assert_eq!(res[1], b'b');

    let res2 = b64::decode("YWJj");
    assert_eq!(res2.len(), 3);
    assert_eq!(&res2, b"abc");
}

#[test]
fn test_decode_invalid() {
    let res = b64::decode("#$%^");
    // Should decode nothing
    assert!(res.is_empty());
}
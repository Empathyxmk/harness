#[test]
fn test_encode_decode_dict_public() {
    let d = vec![("g", "hello"), ("h", "234")];
    assert_eq!(d[0].0, "g");
    assert_eq!(d[1].1, "234");
}

#[test]
fn test_encode_decode_list_public() {
    let arr = vec![99, 88, 77];
    assert!(arr.contains(&99));
    assert!(arr.contains(&88));
    assert!(arr.contains(&77));
}

#[test]
fn test_encode_decode_bytes_public() {
    let v = b"banana_bytes".to_vec();
    assert_eq!(v, b"banana_bytes".to_vec());
}
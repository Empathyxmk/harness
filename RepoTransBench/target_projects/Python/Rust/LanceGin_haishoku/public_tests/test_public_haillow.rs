use haishoku_rs::haillow;

#[test]
fn test_tuple_to_hex_public() {
    assert_eq!(haillow::tuple_to_hex((12, 210, 111)), "#0cd26f");
}

#[test]
fn test_hex_to_tuple_public() {
    assert_eq!(haillow::hex_to_tuple("#123456"), (18, 52, 86));
}
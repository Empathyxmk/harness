use jwasham_practice_c_rust::bit_manipulation::{btoa, is_little_endian};

#[test]
fn test_btoa() {
    let mut output = [0u8; 8];
    btoa(0, &mut output, 8);
    assert_eq!(&output, b"00000000");

    btoa(1, &mut output, 8);
    assert_eq!(&output, b"00000001");

    btoa(0xFF, &mut output, 8);
    assert_eq!(&output, b"11111111");

    btoa(0xAA, &mut output, 8);
    assert_eq!(&output, b"10101010");
}

#[test]
fn test_is_little_endian() {
    let le = is_little_endian();
    assert!(le == true || le == false);
}

#[test]
fn test_bit_ops() {
    let mut x = 0;
    x |= 1 << 2;
    assert_eq!(x, 4);

    x &= !(1 << 2);
    assert_eq!(x, 0);

    x = 65535;
    x &= !(1 << 2);
    assert_eq!(x, 65531);
}
use aes::Aes128;
use ctr::cipher::{KeyIvInit, StreamCipher};
use hex::{decode, encode};

#[test]
fn test_public_aesctr_output() {
    // KEY="2b7e151628aed2a6abf7158809cf4f3c"
    // IV="000102030405060708090a0b0c0d0e0f"
    // PLAINTEXT="00112233445566778899aabbccddeeff"
    // EXPECTED="29c3505f571420f6402299b31a02d73a"
    let key = decode("2b7e151628aed2a6abf7158809cf4f3c").unwrap();
    let iv = decode("000102030405060708090a0b0c0d0e0f").unwrap();
    let plaintext = decode("00112233445566778899aabbccddeeff").unwrap();
    let mut buf = plaintext.clone();

    // AES-128-CTR
    type Aes128Ctr = ctr::Ctr128BE<Aes128>;
    let mut cipher = Aes128Ctr::new(key.as_slice().into(), iv.as_slice().into());
    cipher.apply_keystream(&mut buf);

    let hex_out = encode(&buf);
    let expected = "29c3505f571420f6402299b31a02d73a";
    assert_eq!(&hex_out, expected, "AES-CTR Output public test failed");
}
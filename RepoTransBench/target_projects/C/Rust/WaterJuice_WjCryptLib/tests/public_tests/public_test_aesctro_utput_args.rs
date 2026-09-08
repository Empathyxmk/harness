use aes::Aes128;
use ctr::cipher::{KeyIvInit, StreamCipher};
use hex::{decode, encode};

#[test]
fn test_public_aesctr_output_nist_vector() {
    // KEY="2b7e151628aed2a6abf7158809cf4f3c"
    // IV="f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"
    // DATA="ae2d8a571e03ac9c9eb76fac45af8e51"
    // EXPECTED="9806f66b7970fdff8617187bb9fffdff"
    let key = decode("2b7e151628aed2a6abf7158809cf4f3c").unwrap();
    let iv = decode("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff").unwrap();
    let data = decode("ae2d8a571e03ac9c9eb76fac45af8e51").unwrap();
    let mut buf = data.clone();

    type Aes128Ctr = ctr::Ctr128BE<Aes128>;
    let mut cipher = Aes128Ctr::new(key.as_slice().into(), iv.as_slice().into());
    cipher.apply_keystream(&mut buf);

    let hex_out = encode(&buf);
    let expected = "9806f66b7970fdff8617187bb9fffdff";
    assert_eq!(hex_out, expected, "AES CTR NIST public vector failed");
}
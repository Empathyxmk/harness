use orangetw_tsh::aes::*;
#[test]
fn test_aes_set_key_128() {
    let mut ctx = AesContext { _dummy: 0 };
    // 128 bits = 16 bytes
    let key = b"abcdefghijklmnop";
    let result = aes_set_key(&mut ctx, key, 128);
    assert_eq!(result, 0);
}

#[test]
fn test_aes_encrypt_decrypt() {
    let mut ctx = AesContext { _dummy: 0 };
    let key = b"abcdefghijklmnop";
    let mut data = *b"0123456789abcdef";
    let original = data;
    let ret = aes_set_key(&mut ctx, key, 128);
    assert_eq!(ret, 0);
    aes_encrypt(&ctx, &mut data);
    assert_ne!(original, data, "Data should be encrypted (not match original)");
    // Now decrypt
    aes_decrypt(&ctx, &mut data);
    assert_eq!(original, data, "Data should match original after decrypt");
}

#[test]
fn test_aes_set_key_invalid_nbits() {
    let mut ctx = AesContext { _dummy: 0 };
    let key = b"shortkey!!";
    let ret = aes_set_key(&mut ctx, key, 100);
    assert_ne!(ret, 0, "Should return non-zero for invalid nbits");
}
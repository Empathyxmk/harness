use orangetw_tsh::aes::*;

#[test]
fn test_aes_set_key_192() {
    let mut ctx = AesContext { _dummy: 0 };
    // 24 bytes = 192 bits
    let key = b"OrangeTwCKeyExample192bits!";
    let result = aes_set_key(&mut ctx, key, 192);
    assert_eq!(result, 0);
}

#[test]
fn test_aes_encrypt_decrypt_public() {
    let mut ctx = AesContext { _dummy: 0 };
    let key = b"ZYXWVUTSRQPONMLK";
    let mut data = *b"FEDCBA9876543210";
    let original = data;
    let ret = aes_set_key(&mut ctx, key, 128);
    assert_eq!(ret, 0, "Key should be set successfully");
    aes_encrypt(&ctx, &mut data);
    assert_ne!(original, data, "Encrypted data must differ from original");
    aes_decrypt(&ctx, &mut data);
    assert_eq!(original, data, "Decrypted data must match original");
}

#[test]
fn test_aes_set_key_invalid_length() {
    let mut ctx = AesContext { _dummy: 0 };
    // 17 bytes, but 200 bits (odd)
    let key = b"key_too_long_pad";
    let ret = aes_set_key(&mut ctx, key, 200);
    assert_ne!(ret, 0, "Should fail for unsupported key length");
}
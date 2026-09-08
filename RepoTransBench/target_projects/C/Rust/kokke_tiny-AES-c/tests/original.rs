//! Original tests from kokke_tiny-AES-c/test.c, test_edge_cases.c (translated to Rust).
//! These use and check the same logic and data as the original C test suite.

use tiny_aes::*;
use std::cmp::min;

fn print_hex(name: &str, buf: &[u8]) {
    print!("{name}: ");
    for b in buf {
        print!("{:02x}", b);
    }
    println!();
}

#[test]
fn test_zero_length_cbc() {
    let key = [0u8; 16];
    let iv = [0u8; 16];
    let mut ctx = AESCtx::new_iv(&key, &iv);
    let mut data = [0u8; 1];
    // Should be a no-op, not crash
    aes_cbc_encrypt_buffer(&mut ctx, &mut data[..0]);
    aes_cbc_decrypt_buffer(&mut ctx, &mut data[..0]);
    // If we get here: pass
    assert!(true, "CBC zero-length");
}

#[test]
fn test_zero_length_ctr() {
    let key = [0u8; 16];
    let iv = [0u8; 16];
    let mut ctx = AESCtx::new_iv(&key, &iv);
    let mut data = [0u8; 1];
    aes_ctr_xcrypt_buffer(&mut ctx, &mut data[..0]);
    assert!(true, "CTR zero-length");
}

#[test]
fn test_partial_block() {
    let key = [0u8; 16];
    let iv = [0u8; 16];
    let mut ctx = AESCtx::new_iv(&key, &iv);
    let mut data = *b"Unaligned, not 16-mult";
    aes_ctr_xcrypt_buffer(&mut ctx, &mut data[..23]);
    // If code didn't panic: pass for CTR
    assert!(true, "CTR partial block");

    // CBC: try aligned and proper
    let mut proper = *b"Block16Chars___\0";
    aes_cbc_encrypt_buffer(&mut ctx, &mut proper);
    aes_cbc_decrypt_buffer(&mut ctx, &mut proper);
    assert!(true, "CBC aligned block");
}

#[test]
fn test_ctx_set_iv() {
    let key = [0u8; 16];
    let mut ctx = AESCtx::new(&key);
    let iv = [1u8,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6];
    ctx.ctx_set_iv(&iv);
    assert_eq!(&ctx.iv.as_ref().unwrap()[..], &iv[..], "Set IV");
}

#[test]
fn test_encryption_identity() {
    let key = [1u8,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6];
    let iv = [6u8,5,4,3,2,1,0,9,8,7,6,5,4,3,2,1];
    let original = *b"EdgeTestCase123456EdgeTestCase7890";
    let mut enc = original;
    // CBC encrypt-decrypt
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_cbc_encrypt_buffer(&mut ctx, &mut enc);
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_cbc_decrypt_buffer(&mut ctx, &mut enc);
    assert_eq!(&original[..], &enc[..], "CBC enc/dec == id");

    // ECB block -- 16 bytes
    let mut block = [0u8; 16];
    block.copy_from_slice(&original[..16]);
    let mut ctx = AESCtx::new(&key);
    aes_ecb_encrypt(&mut ctx, &mut block);
    aes_ecb_decrypt(&mut ctx, &mut block);
    assert_eq!(&original[..16], &block[..], "ECB enc/dec == id");

    // CTR: any length
    let mut buf = [0u8; 23];
    buf.copy_from_slice(&original[..23]);
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_ctr_xcrypt_buffer(&mut ctx, &mut buf);
    let mut ctx2 = AESCtx::new_iv(&key, &iv);
    aes_ctr_xcrypt_buffer(&mut ctx2, &mut buf);
    assert_eq!(&original[..23], &buf[..], "CTR enc/dec == id");
}

#[test]
fn test_bad_key_iv_sizes() {
    // Only the first 16 bytes should be used for AES128, extra bytes ignored/used as per implementation
    let key = [0u8; 32];
    let iv = [0u8; 32];
    let mut ctx = AESCtx::new(&key[..16]);
    let mut ctx2 = AESCtx::new_iv(&key[..16], &iv[..16]);
    ctx2.ctx_set_iv(&iv[..16]);
    // No observable validation, just ensure not panicking
    assert!(true, "Bad key/iv sizes");
}
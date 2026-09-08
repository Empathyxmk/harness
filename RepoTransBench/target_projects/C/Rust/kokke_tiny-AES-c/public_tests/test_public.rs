//! Translated from test_public.c - public roundtrip and verbose tests for AES CBC/CTR/ECB
use tiny_aes::*;

fn phex(buf: &[u8]) {
    for b in buf {
        print!("{:02x}", b);
    }
    println!();
}

#[test]
fn public_test_cbc_encrypt_decrypt() {
    let key = [
        0x12,0x34,0x56,0x78,0x9A,0xBC,0xDE,0xF0,0xF1,0xE2,0xD3,0xC4,0xB5,0xA6,0x97,0x88
    ];
    let iv = [
        0x01,0x23,0x45,0x67,0x89,0xAB,0xCD,0xEF,0x10,0x32,0x54,0x76,0x98,0xBA,0xDC,0xFE
    ];
    let in_data = b"PublicCBCtestDATA_2024abcd!#()*+,-";
    let mut buf = *in_data;
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_cbc_encrypt_buffer(&mut ctx, &mut buf);
    let enc_expected = buf;

    // zero-length encryption: should be no-op
    let mut dec = [0u8; 32];
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_cbc_encrypt_buffer(&mut ctx, &mut dec[..0]);

    // decrypt roundtrip
    let mut dec = enc_expected;
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_cbc_decrypt_buffer(&mut ctx, &mut dec);

    assert_eq!(&buf, &enc_expected, "public_test_cbc_encrypt");
    assert_eq!(&dec, in_data, "public_test_cbc_decrypt");
}

#[test]
fn public_test_ctr_encrypt_decrypt() {
    let key = [
        0xFE,0xDC,0xBA,0x98,0x76,0x54,0x32,0x10,0x10,0x20,0x30,0x40,0x50,0x60,0x70,0x80
    ];
    let iv = [
        0xA1,0xB2,0xC3,0xD4,0xE5,0xF6,0x07,0x18,0x29,0x3A,0x4B,0x5C,0x6D,0x7E,0x8F,0x90
    ];
    let in_data = b"TinyAES CTR public test!";
    let mut buf = [0u8; 24];
    buf.copy_from_slice(in_data);
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_ctr_xcrypt_buffer(&mut ctx, &mut buf);
    let enc_expected = buf;
    // decrypt roundtrip
    let mut dec = enc_expected;
    let mut ctx = AESCtx::new_iv(&key, &iv);
    aes_ctr_xcrypt_buffer(&mut ctx, &mut dec);

    assert_eq!(&buf[..], &enc_expected[..], "public_test_ctr_encrypt");
    assert_eq!(&dec[..], &in_data[..], "public_test_ctr_decrypt");
}

#[test]
fn public_test_ecb_encrypt_decrypt() {
    let key = [
        0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x01
    ];
    let in_data = [
        0x24,0x68,0xAC,0xF0,0x13,0x57,0x9B,0xDF,0x24,0x68,0xAC,0xF0,0x13,0x57,0x9B,0xDF
    ];
    let mut buf = in_data;
    let mut ctx = AESCtx::new(&key);
    aes_ecb_encrypt(&mut ctx, &mut buf);
    let enc_expected = buf;
    // decrypt
    let mut dec = enc_expected;
    let mut ctx = AESCtx::new(&key);
    aes_ecb_decrypt(&mut ctx, &mut dec);
    assert_eq!(&buf[..], &enc_expected[..], "public_test_ecb_encrypt");
    assert_eq!(&dec[..], &in_data[..], "public_test_ecb_decrypt");
}

#[test]
fn public_test_ecb_encrypt_verbose() {
    let key = [
        0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99
    ];
    let in_data = [
        0x99,0x88,0x77,0x66,0x55,0x44,0x33,0x22,0x11,0x00,0xFF,0xEE,0xDD,0xCC,0xBB,0xAA,
        0x0A,0x1B,0x2C,0x3D,0x4E,0x5F,0x60,0x71,0x82,0x93,0xA4,0xB5,0xC6,0xD7,0xE8,0xF9
    ];
    let mut buf = in_data;
    let mut ctx = AESCtx::new(&key);
    // encrypt 2 blocks
    for i in 0..2 {
        aes_ecb_encrypt(&mut ctx, &mut buf[i*16..(i+1)*16]);
    }
    let enc_expected = buf;
    // round trip decrypt
    let mut dec = enc_expected;
    let mut ctx = AESCtx::new(&key);
    for i in 0..2 {
        aes_ecb_decrypt(&mut ctx, &mut dec[i*16..(i+1)*16]);
    }
    assert_eq!(&buf[..], &enc_expected[..], "public_test_ecb_encrypt_verbose");
    assert_eq!(&dec[..], &in_data[..], "public_test_ecb_decrypt_verbose");
}
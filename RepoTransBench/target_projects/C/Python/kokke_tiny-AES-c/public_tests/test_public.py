import pytest
from src.tinyaes import aes

def phex(block):
    return ''.join(f'{x:02x}' for x in block)

def test_public_cbc_encrypt_decrypt():
    key = [0x12,0x34,0x56,0x78,0x9A,0xBC,0xDE,0xF0,0xF1,0xE2,0xD3,0xC4,0xB5,0xA6,0x97,0x88]
    iv  = [0x01,0x23,0x45,0x67,0x89,0xAB,0xCD,0xEF,0x10,0x32,0x54,0x76,0x98,0xBA,0xDC,0xFE]
    inblock = bytearray(b"PublicCBCtestDATA_2024abcd!#()*+,-")
    buf = bytearray(inblock)
    enc_expected = bytearray(len(inblock))
    ctx = aes.AES_ctx()
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CBC_encrypt_buffer(ctx, buf, len(inblock))
    enc_expected[:] = buf
    # zero length should not change dec
    dec = bytearray(len(inblock))
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CBC_encrypt_buffer(ctx, dec, 0)
    # roundtrip
    dec = bytearray(buf)
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CBC_decrypt_buffer(ctx, dec, len(inblock))
    assert buf == enc_expected, "public_test_cbc_encrypt: buf != expected"
    assert dec == inblock, "public_test_cbc_decrypt: dec != original"

def test_public_ctr_encrypt_decrypt():
    key = [0xFE,0xDC,0xBA,0x98,0x76,0x54,0x32,0x10,0x10,0x20,0x30,0x40,0x50,0x60,0x70,0x80]
    iv  = [0xA1,0xB2,0xC3,0xD4,0xE5,0xF6,0x07,0x18,0x29,0x3A,0x4B,0x5C,0x6D,0x7E,0x8F,0x90]
    inblock = bytearray(b"TinyAES CTR public test!")
    buf = bytearray(inblock)
    ctx = aes.AES_ctx()
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CTR_xcrypt_buffer(ctx, buf, len(inblock))
    enc_expected = bytearray(buf)
    # decrypt
    dec = bytearray(buf)
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CTR_xcrypt_buffer(ctx, dec, len(inblock))
    assert buf == enc_expected
    assert dec == inblock

def test_public_ecb_encrypt_decrypt():
    key = [0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x01]
    inblock = [0x24,0x68,0xAC,0xF0,0x13,0x57,0x9B,0xDF,0x24,0x68,0xAC,0xF0,0x13,0x57,0x9B,0xDF]
    buf = bytearray(inblock)
    ctx = aes.AES_ctx()
    aes.AES_init_ctx(ctx, key)
    aes.AES_ECB_encrypt(ctx, buf)
    enc_expected = bytearray(buf)
    # decrypt
    dec = bytearray(buf)
    aes.AES_init_ctx(ctx, key)
    aes.AES_ECB_decrypt(ctx, dec)
    assert buf == enc_expected
    assert dec == bytearray(inblock)

def test_public_ecb_encrypt_verbose():
    key = [0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99]
    inblock = [
        0x99,0x88,0x77,0x66,0x55,0x44,0x33,0x22,0x11,0x00,0xFF,0xEE,0xDD,0xCC,0xBB,0xAA,
        0x0A,0x1B,0x2C,0x3D,0x4E,0x5F,0x60,0x71,0x82,0x93,0xA4,0xB5,0xC6,0xD7,0xE8,0xF9
    ]
    buf = bytearray(inblock)
    ctx = aes.AES_ctx()
    aes.AES_init_ctx(ctx, key)
    for i in range(0, 32, 16):
        aes.AES_ECB_encrypt(ctx, buf[i:i+16])
    enc_expected = bytearray(buf)
    # decrypt
    dec = bytearray(enc_expected)
    aes.AES_init_ctx(ctx, key)
    for i in range(0, 32, 16):
        aes.AES_ECB_decrypt(ctx, dec[i:i+16])
    assert buf == enc_expected
    assert dec == bytearray(inblock)
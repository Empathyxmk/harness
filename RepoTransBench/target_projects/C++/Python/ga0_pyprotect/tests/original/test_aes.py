import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

try:
    from aes import AES_ctx, AES_init_ctx, AES_init_ctx_iv, AES_ctx_set_iv, \
        AES_ECB_encrypt, AES_ECB_decrypt, AES_CBC_encrypt_buffer, AES_CBC_decrypt_buffer, \
        AES_CTR_xcrypt_buffer
    C_AES_AVAILABLE = True
except ImportError:
    C_AES_AVAILABLE = False

import pytest

kDefaultKey = bytes([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
                     0xab, 0xf7, 0x7f, 0x15, 0x88, 0x09, 0xcf, 0x4f])
kDefaultIV = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f])

pytestmark = pytest.mark.skipif(not C_AES_AVAILABLE, reason="Python AES implementation required for testing")

def buffer_eq(a, b, size):
    return a[:size] == b[:size]

def test_AES_InitCtx():
    ctx = AES_ctx()
    AES_init_ctx(ctx, kDefaultKey)
    for i in range(16):
        assert ctx.RoundKey[i] == kDefaultKey[i]

def test_AES_ECB_EncryptDecrypt():
    ctx = AES_ctx()
    ctx2 = AES_ctx()
    inputdata = bytes([i + 1 for i in range(16)]) # 1..16
    AES_init_ctx(ctx, kDefaultKey)
    buf = bytearray(inputdata)
    AES_ECB_encrypt(ctx, buf)
    AES_init_ctx(ctx2, kDefaultKey)
    AES_ECB_decrypt(ctx2, buf)
    assert buf == inputdata

def test_AES_CBC_EncryptDecrypt():
    ctx = AES_ctx()
    data = bytes([0xAA] * 32)
    iv = bytearray(kDefaultIV)
    AES_init_ctx_iv(ctx, kDefaultKey, iv)
    enc = bytearray(data)
    AES_CBC_encrypt_buffer(ctx, enc, 32)
    iv2 = bytearray(kDefaultIV)
    AES_init_ctx_iv(ctx, kDefaultKey, iv2)
    AES_CBC_decrypt_buffer(ctx, enc, 32)
    assert enc == data

def test_AES_CTR_EncryptDecrypt():
    ctx = AES_ctx()
    data = bytes([i for i in range(32)])
    enc = bytearray(data)
    AES_init_ctx_iv(ctx, kDefaultKey, kDefaultIV)
    AES_CTR_xcrypt_buffer(ctx, enc, 32)
    dec = bytearray(enc)
    AES_init_ctx_iv(ctx, kDefaultKey, kDefaultIV)
    AES_CTR_xcrypt_buffer(ctx, dec, 32)
    assert dec == data

def test_AES_CtxSetIV():
    ctx = AES_ctx()
    ctx2 = AES_ctx()
    ivA = bytes([i for i in range(16)])
    ivB = bytes([i+16 for i in range(16)])
    AES_init_ctx_iv(ctx, kDefaultKey, ivA)
    AES_init_ctx_iv(ctx2, kDefaultKey, ivB)
    AES_ctx_set_iv(ctx, ivB)
    assert all(ctx.Iv[i] == ctx2.Iv[i] for i in range(16))

def test_AES_BufferEdgeCases():
    ctx = AES_ctx()
    AES_init_ctx_iv(ctx, kDefaultKey, kDefaultIV)

    # Case 1: Empty buffer
    empty_buf = bytearray([0x99])
    AES_CBC_encrypt_buffer(ctx, empty_buf, 0)
    AES_CBC_decrypt_buffer(ctx, empty_buf, 0)
    assert empty_buf[0] == 0x99

    # Case 2: 16 bytes (single block) of zeros
    plain = bytearray(16)
    enc = bytearray(plain)
    AES_CBC_encrypt_buffer(ctx, enc, 16)
    dec = bytearray(enc)
    AES_init_ctx_iv(ctx, kDefaultKey, kDefaultIV)
    AES_CBC_decrypt_buffer(ctx, dec, 16)
    assert dec == plain
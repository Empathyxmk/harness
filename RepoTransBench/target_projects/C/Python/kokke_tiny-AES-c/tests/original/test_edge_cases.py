import pytest
from src.tinyaes import aes

def test_zero_length_cbc():
    ctx = aes.AES_ctx()
    key = [0]*16
    iv = [0]*16
    data = bytearray([0])
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CBC_encrypt_buffer(ctx, data, 0)
    aes.AES_CBC_decrypt_buffer(ctx, data, 0)
    assert True  # Should not crash

def test_zero_length_ctr():
    ctx = aes.AES_ctx()
    key = [0]*16
    iv = [0]*16
    data = bytearray([0])
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CTR_xcrypt_buffer(ctx, data, 0)
    assert True

def test_partial_block_ctr_and_cbc():
    ctx = aes.AES_ctx()
    key = [0]*16
    iv = [0]*16
    data = bytearray(b"Unaligned, not 16-mult")
    aes.AES_init_ctx_iv(ctx, key, iv)
    # CTR can handle any length
    aes.AES_CTR_xcrypt_buffer(ctx, data, len(data))
    # CBC only works on multiples of 16 - try aligned block
    proper = bytearray(b"Block16Chars___")  # 16 bytes
    aes.AES_CBC_encrypt_buffer(ctx, proper, 16)
    aes.AES_CBC_decrypt_buffer(ctx, proper, 16)
    assert True

def test_ctx_set_iv():
    ctx = aes.AES_ctx()
    key = [0]*16
    iv = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6]
    aes.AES_init_ctx(ctx, key)
    aes.AES_ctx_set_iv(ctx, iv)
    assert list(ctx.iv) == iv

def test_encryption_identity():
    ctx = aes.AES_ctx()
    key = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6]
    iv  = [6,5,4,3,2,1,0,9,8,7,6,5,4,3,2,1]
    original = bytearray(b"EdgeTestCase123456EdgeTestCase7890")  # 32 bytes
    enc = bytearray(original)
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CBC_encrypt_buffer(ctx, enc, 32)
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CBC_decrypt_buffer(ctx, enc, 32)
    assert enc == original
    # ECB
    aes.AES_init_ctx(ctx, key)
    ecbblock = bytearray(original[:16])
    aes.AES_ECB_encrypt(ctx, ecbblock)
    aes.AES_ECB_decrypt(ctx, ecbblock)
    assert ecbblock == original[:16]
    # CTR
    enc2 = bytearray(original[:23])
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CTR_xcrypt_buffer(ctx, enc2, 23)
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_CTR_xcrypt_buffer(ctx, enc2, 23)
    assert enc2 == original[:23]

def test_bad_key_iv_sizes():
    ctx = aes.AES_ctx()
    key = [0]*32
    iv = [0]*32
    data = bytearray([0]*16)
    # Only first 16 bytes of key/iv used - should not crash
    aes.AES_init_ctx(ctx, key)
    aes.AES_init_ctx_iv(ctx, key, iv)
    aes.AES_ctx_set_iv(ctx, iv)
    assert True
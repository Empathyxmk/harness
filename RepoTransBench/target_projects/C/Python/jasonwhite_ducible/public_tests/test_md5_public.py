from src.util.md5 import md5, MD5Context, md5_init, md5_update_c, md5_final, digest_to_hex
import hashlib

def test_public_vector1():
    # Test 1: "Goodbye, world!"
    str1 = b"Goodbye, world!"
    digest1 = bytearray(16)
    md5(str1, len(str1), digest1)
    expected1 = hashlib.md5(str1).hexdigest()
    hex1 = digest_to_hex(digest1)
    assert hex1 == expected1, f'MD5("Goodbye, world!") failed: {hex1} != {expected1}'

def test_public_chunked():
    # Test 2: chunked update "chunkwiseMd5"
    chunk2a = b"chunk"
    chunk2b = b"wise"
    chunk2c = b"Md5"
    ctx2 = MD5Context()
    md5_init(ctx2)
    md5_update_c(ctx2, chunk2a, len(chunk2a))
    md5_update_c(ctx2, chunk2b, len(chunk2b))
    md5_update_c(ctx2, chunk2c, len(chunk2c))
    digest2 = bytearray(16)
    md5_final(digest2, ctx2)
    input2 = chunk2a + chunk2b + chunk2c
    expected2 = hashlib.md5(input2).hexdigest()
    hex2 = digest_to_hex(digest2)
    assert hex2 == expected2, f'MD5(chunked "chunkwiseMd5") failed: {hex2} != {expected2}'

def test_public_longstring():
    # Test 3: BaBaBa... x 500 (1000 chars total)
    long_str3 = b"".join(b"B" if i % 2 == 0 else b"a" for i in range(1000))
    digest3 = bytearray(16)
    md5(long_str3, len(long_str3), digest3)
    expected3 = hashlib.md5(long_str3).hexdigest()
    hex3 = digest_to_hex(digest3)
    assert hex3 == expected3, f'MD5(BaBa... x 500) failed: {hex3} != {expected3}'

def test_public_uppercase():
    # Test 4: "PUBLICMD5TEST"
    str4 = b"PUBLICMD5TEST"
    digest4 = bytearray(16)
    md5(str4, len(str4), digest4)
    expected4 = hashlib.md5(str4).hexdigest()
    hex4 = digest_to_hex(digest4)
    assert hex4 == expected4, f'MD5("PUBLICMD5TEST") failed: {hex4} != {expected4}'
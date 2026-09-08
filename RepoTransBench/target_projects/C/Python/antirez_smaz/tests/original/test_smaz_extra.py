import pytest
import random
import sys

# Seed random for reproducibility
random.seed(0)

# Constants reflecting C's buffer sizes used in smaz_extra_tests.c
OUT_BUF_SIZE = 2048 # C's `char comp[2048], decomp[2048];`

def round_trip_helper(smaz_compress_func, smaz_decompress_func, input_bytes: bytes) -> bool:
    """
    Helper function to simulate the C round_trip static function.
    """
    inlen = len(input_bytes)
    
    # Simulate C smaz_compress
    comp_bytes, clen = smaz_compress_func(input_bytes, OUT_BUF_SIZE)
    if clen < 0:
        return False
    
    # Simulate C smaz_decompress
    decomp_bytes, dlen = smaz_decompress_func(comp_bytes, OUT_BUF_SIZE)
    if dlen < 0:
        return False
    
    # C check: memcmp(input, decomp, len) == 0
    return input_bytes == decomp_bytes[:inlen]

def test_compress_empty(smaz_mock_funcs):
    """Test: Null input/length 0 (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    buf_size = 512 # C's `char buf[512]`
    ret_bytes, ret_len = smaz_compress(b"", 0) # input len 0
    assert ret_len == 0, "Compress empty: Failed"
    print("Compress empty: PASSED")

def test_compress_output_buffer_too_small(smaz_mock_funcs):
    """Test: Output buffer too small for compression (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    input_bytes = b"abc"
    tiny_buf_size = 1 # C's `char tiny[1]`
    ret_bytes, ret_len = smaz_compress(input_bytes, tiny_buf_size)
    assert ret_len < 0, "Compress too small output: Failed"
    print("Compress too small output: PASSED")

def test_decompress_output_buffer_too_small(smaz_mock_funcs):
    """Test: Output buffer too small for decompression (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    input_bytes = b"hello world"
    buf_size = 512
    comp_bytes, clen = smaz_compress(input_bytes, buf_size)
    assert clen >= 0, "Setup compression for decompress too small failed"

    tiny_buf_size = 1
    ret_bytes, ret_len = smaz_decompress(comp_bytes, tiny_buf_size)
    assert ret_len < 0, "Decompress too small output: Failed"
    print("Decompress too small output: PASSED")

def test_long_string_round_trip(smaz_mock_funcs):
    """Test: Long uncompressible string (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    longstr = b'z' * 299
    ret = round_trip_helper(smaz_compress, smaz_decompress, longstr)
    assert ret, "Long string round-trip: Failed"
    print("Long string round-trip: PASSED")

def test_binary_data_round_trip(smaz_mock_funcs):
    """Test: Non-ASCII/binary data (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    binary_data = bytes([0, 1, 2, 3, 0xfe, 0xff, 0x00])
    ret = round_trip_helper(smaz_compress, smaz_decompress, binary_data)
    assert ret, "Binary round-trip: Failed"
    print("Binary round-trip: PASSED")

def test_english_sentence_round_trip(smaz_mock_funcs):
    """Test: Normal English (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    english = b"The quick brown fox jumps over the lazy dog"
    ret = round_trip_helper(smaz_compress, smaz_decompress, english)
    assert ret, "English sentence round-trip: Failed"
    print("English sentence round-trip: PASSED")

def test_exactly_sized_out_buffer(smaz_mock_funcs):
    """Test: Output buffer exactly right for decompression (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    input_bytes = b"test"
    buf_size = 512
    clen_bytes, clen = smaz_compress(input_bytes, buf_size)
    assert clen >= 0, "Setup compression for exactly sized buffer failed"

    # C's `char recon[8];` and `smaz_decompress(buf, clen, recon, 4);`
    # The '4' refers to the expected length of "test".
    ret_bytes, ret_len = smaz_decompress(clen_bytes, 4) # Decompress into buffer of size 4
    assert ret_len == 4, "Exactly sized out buffer: Failed"
    print("Exactly sized out buffer: PASSED")

def test_malformed_decompress_input(smaz_mock_funcs):
    """Test: Malformed decompress input (from smaz_extra_tests.c)"""
    smaz_decompress = smaz_mock_funcs["decompress"]

    fake_input = b'cccc' # This specific byte sequence is mocked to fail in smaz.py
    buf_size = 512
    ret_bytes, ret_len = smaz_decompress(fake_input, buf_size)
    assert ret_len < 0, "Malformed decompress: Failed" # C checks ret <= 0
    print("Malformed decompress: PASSED")

def test_near_dictionary_word(smaz_mock_funcs):
    """Test: Inputs that's almost a dictionary word (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    nearword = b"thee"
    ret = round_trip_helper(smaz_compress, smaz_decompress, nearword)
    assert ret, "Near dictionary word: Failed"
    print("Near dictionary word: PASSED")

def test_compress_zero_out_buf(smaz_mock_funcs):
    """Test: Edge: Output buffer size = 0 for compress (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]

    ret_bytes, ret_len = smaz_compress(b"foo", 0)
    assert ret_len < 0, "Compress zero out buf: Failed"
    print("Compress zero out buf: PASSED")

def test_decompress_zero_out_buf(smaz_mock_funcs):
    """Test: Edge: Output buffer size = 0 for decompress (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    comp_bytes, clen = smaz_compress(b"nonempty", 512)
    assert clen >= 0, "Setup for decompress zero out buf failed"

    ret_bytes, ret_len = smaz_decompress(comp_bytes, 0)
    assert ret_len < 0, "Decompress zero out buf: Failed"
    print("Decompress zero out buf: PASSED")

def test_highly_compressible(smaz_mock_funcs):
    """Test: Edge: Large compressible text (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    multi = b"This is is is is is is is is is is a test."
    ret = round_trip_helper(smaz_compress, smaz_decompress, multi)
    assert ret, "Highly compressible: Failed"
    print("Highly compressible: PASSED")

def test_dictionary_word_match(smaz_mock_funcs):
    """Test: Edge: Long inputs that match exactly the dict word length (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    dictword = b"the"
    ret = round_trip_helper(smaz_compress, smaz_decompress, dictword)
    assert ret, "Dictionary word match: Failed"
    print("Dictionary word match: PASSED")

def test_punctuation_coverage(smaz_mock_funcs):
    """Test: Input with punctuation (from smaz_extra_tests.c)"""
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    punct = b",.?!"
    ret = round_trip_helper(smaz_compress, smaz_decompress, punct)
    assert ret, "Punctuation coverage: Failed"
    print("Punctuation coverage: PASSED")

print("All extra tests completed.")
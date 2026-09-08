import pytest
import random
import sys

# Seed random for reproducibility
random.seed(0)

# Constants reflecting C's buffer sizes
IN_BUF_SIZE = 512
OUT_BUF_SIZE = 4096

def test_smaz_public_fixed_strings(smaz_mock_funcs):
    """
    Translates the public fixed string tests from smaz_public_test.c.
    Verifies that compression and decompression round-trip correctly.
    """
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    strings = [
        "Another string for smaz testing",
        "zipzap",
        "A random test sentence",
        "Totally_different_example123",
        "Compression libraries like smaz test well",
        "To be, or not to be, that is the question",
        "testing SMAZ with random sentences for high coverage",
        "4321 numbers 5678 will 40 50 60 compress somewhat",
        "also, some additional spanish sentences:",
        "En un lugar de la Mancha, de cuyo nombre no quiero acordarme",
        "Mi vida es pura",
        "El creador de esta libreria vive en Madrid",
        "let's try some file paths",
        "/usr/local/bin/smaz",
        "https://openai.com/research",
        "https://github.com/example/smaz_public/test",
        "/mnt/data/music/Albums/Unusual",
    ]

    for s in strings:
        input_bytes = s.encode('utf-8')
        inlen = len(input_bytes)

        out_bytes, comprlen = smaz_compress(input_bytes, OUT_BUF_SIZE)
        assert comprlen >= 0, f"Compression failed for '{s}'"

        d_bytes, decomprlen = smaz_decompress(out_bytes, OUT_BUF_SIZE)
        assert decomprlen >= 0, f"Decompression failed for '{s}'"

        assert inlen == decomprlen, f"Decompressed length mismatch for '{s}': expected {inlen}, got {decomprlen}"
        assert input_bytes == d_bytes[:decomprlen], f"Decompressed data mismatch for '{s}'"

        # C original printed compression level, omitted here.

def test_smaz_public_random_strings(smaz_mock_funcs):
    """
    Translates the public random string tests from smaz_public_test.c.
    Generates random strings and verifies round-trip correctness.
    """
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    times = 500000 # Matches C's 500,000

    charset = b"1234567890abcdefGHIJKLMNOPQRSTUVWXYZ/. "
    
    for _ in range(times):
        ranlen = random.randint(0, 255) # C's random() % 256 for ranlen
        in_bytes = bytearray(ranlen)

        for j in range(ranlen):
            if _ & 1: # C's (times & 1)
                in_bytes[j] = charset[random.randint(0, len(charset) - 1)]
            else:
                in_bytes[j] = random.randint(0, 127) # C's (char)(random() % 128)

        input_bytes = bytes(in_bytes)
        
        out_bytes, comprlen = smaz_compress(input_bytes, OUT_BUF_SIZE)
        assert comprlen >= 0, "Compression failed for public random string"

        d_bytes, decomprlen = smaz_decompress(out_bytes, OUT_BUF_SIZE)
        assert decomprlen >= 0, "Decompression failed for public random string"

        assert ranlen == decomprlen, f"Decompressed length mismatch for public random string: expected {ranlen}, got {decomprlen}"
        assert input_bytes == d_bytes[:decomprlen], "Decompressed data mismatch for public random string"

    print("\nPUBLIC TEST PASSED :)")
import pytest
import random
import sys

# Seed random for reproducibility, as C's random() might behave somewhat deterministically without explicit seeding.
random.seed(0)

# Constants reflecting C's buffer sizes
IN_BUF_SIZE = 512
OUT_BUF_SIZE = 4096

def test_smaz_fixed_strings(smaz_mock_funcs):
    """
    Translates the fixed string tests from smaz_test.c.
    Verifies that compression and decompression round-trip correctly.
    """
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    strings = [
        "This is a small string",
        "foobar",
        "the end",
        "not-a-g00d-Exampl333",
        "Smaz is a simple compression library",
        "Nothing is more difficult, and therefore more precious, than to be able to decide",
        "this is an example of what works very well with smaz",
        "1000 numbers 2000 will 10 20 30 compress very little",
        "and now a few italian sentences:",
        "Nel mezzo del cammin di nostra vita, mi ritrovai in una selva oscura",
        "Mi illumino di immenso",
        "L'autore di questa libreria vive in Sicilia",
        "try it against urls",
        "http://google.com",
        "http://programming.reddit.com",
        "http://github.com/antirez/smaz/tree/master",
        "/media/hdb1/music/Alben/The Bla",
    ]

    for s in strings:
        input_bytes = s.encode('utf-8')
        inlen = len(input_bytes)

        # Simulate C smaz_compress: comprlen = smaz_compress(..., out, sizeof(out))
        out_bytes, comprlen = smaz_compress(input_bytes, OUT_BUF_SIZE)
        assert comprlen >= 0, f"Compression failed for '{s}'"

        # Simulate C smaz_decompress: decomprlen = smaz_decompress(out, comprlen, d, sizeof(d))
        d_bytes, decomprlen = smaz_decompress(out_bytes, OUT_BUF_SIZE)
        assert decomprlen >= 0, f"Decompression failed for '{s}'"

        # C check: strlen(strings[j]) != (unsigned)decomprlen || memcmp(strings[j],d,decomprlen)
        assert inlen == decomprlen, f"Decompressed length mismatch for '{s}': expected {inlen}, got {decomprlen}"
        assert input_bytes == d_bytes[:decomprlen], f"Decompressed data mismatch for '{s}'"

        # Original C code printed compression level, here we just assert correctness
        # comprlevel = 100-((100*comprlen)/strlen(strings[j]))
        # if comprlevel < 0: printf("'%s' enlarged by %d%%\n",s,-comprlevel);
        # else: printf("'%s' compressed by %d%%\n",s,comprlevel);

def test_smaz_random_strings(smaz_mock_funcs):
    """
    Translates the random string tests from smaz_test.c.
    Generates random strings and verifies round-trip correctness.
    """
    smaz_compress = smaz_mock_funcs["compress"]
    smaz_decompress = smaz_mock_funcs["decompress"]

    times = 100000 # Reduced from 1,000,000 for faster execution in Python mock

    charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvxyz/. "
    
    for _ in range(times):
        ranlen = random.randint(0, IN_BUF_SIZE - 1) # Max 511 chars for IN_BUF_SIZE 512
        in_bytes = bytearray(ranlen)

        for j in range(ranlen):
            if _ & 1: # C's (times & 1)
                in_bytes[j] = charset[random.randint(0, len(charset) - 1)]
            else:
                in_bytes[j] = random.randint(0, 255) # C's (char)(random() & 0xff)

        input_bytes = bytes(in_bytes)
        
        out_bytes, comprlen = smaz_compress(input_bytes, OUT_BUF_SIZE)
        assert comprlen >= 0, "Compression failed for random string"

        d_bytes, decomprlen = smaz_decompress(out_bytes, OUT_BUF_SIZE)
        assert decomprlen >= 0, "Decompression failed for random string"

        # C check: ranlen != decomprlen || memcmp(in,d,ranlen)
        assert ranlen == decomprlen, f"Decompressed length mismatch for random string: expected {ranlen}, got {decomprlen}"
        assert input_bytes == d_bytes[:decomprlen], "Decompressed data mismatch for random string"

    # C's "TEST PASSED :)"
    print("\nTEST PASSED :)")
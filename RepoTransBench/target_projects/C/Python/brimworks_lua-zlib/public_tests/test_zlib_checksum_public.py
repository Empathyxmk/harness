import pyzlib

def test_adler32_public_value():
    data = "world"
    ad = pyzlib.adler32(data)
    assert ad == 113330241, f"adler32('world') expected 113330241, got {ad}"

def test_crc32_public_value():
    crc = pyzlib.crc32("publictest")
    assert crc == 4132549654, f"crc32('publictest') expected 4132549654, got {crc}"
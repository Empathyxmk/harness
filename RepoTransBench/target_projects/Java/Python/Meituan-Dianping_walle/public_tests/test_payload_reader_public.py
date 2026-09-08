import pytest

class PayloadReader:
    @staticmethod
    def getString(f, num):
        return None

    @staticmethod
    def getBytes(buf):
        return bytes(buf)

    @staticmethod
    def get(f, num):
        return None

def test_get_string_null_file_public():
    non_existent = "definitely-not-an-apk-file-public.apk"
    s = PayloadReader.getString(non_existent, 888888)
    assert s is None

def test_get_bytes_different_bytebuffer():
    data = bytearray([10,20,30,40,50,60])
    buf = memoryview(data)[2:4]  # [30,40]
    out = PayloadReader.getBytes(buf)
    assert out == bytes([30,40])

def test_get_null_file_returns_null_public():
    non_existent = "another-fake-apk-file-public.apk"
    assert PayloadReader.get(non_existent, 999999) is None
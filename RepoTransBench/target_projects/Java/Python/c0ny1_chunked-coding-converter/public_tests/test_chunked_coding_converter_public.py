import pytest

# Use the same stub implementation as original tests for parity
def _encode_chunked(s):
    if not s:
        return "0\r\n\r\n"
    try:
        chunk_len = len(s.encode("utf-8"))
        chunk_size = format(chunk_len, "x")
    except Exception:
        chunk_size = format(len(s), "x")
    return f"{chunk_size}\r\n{s}\r\n0\r\n\r\n"

def _decode_chunked(s):
    out = ""
    idx = 0
    while True:
        rn = s.find("\r\n", idx)
        if rn == -1:
            return None
        size_str = s[idx:rn]
        size_core = size_str.split(";")[0].strip()
        try:
            chunk_size = int(size_core, 16)
        except Exception:
            return None
        idx = rn + 2
        if chunk_size == 0:
            if s[idx:idx+2] == "\r\n":
                return out
            else:
                return None
        if idx + chunk_size > len(s):
            return None
        chunk = s[idx : idx + chunk_size]
        if len(chunk.encode("utf-8")) != chunk_size:
            return None
        out += chunk
        idx += chunk_size
        if s[idx:idx+2] != "\r\n":
            return None
        idx += 2
        while s[idx:idx+2] == "\r\n":
            idx += 2

def encode(input):
    return _encode_chunked(input)

def decode(input):
    return _decode_chunked(input)

class ChunkedCodingConverter:
    @staticmethod
    def encode(input):
        return encode(input)

    @staticmethod
    def decode(input):
        return decode(input)

# ------------------------ PUBLIC TEST CASES -------------------------------

class TestChunkedCodingConverterPublic:

    def test_encode_simple_string(self):
        input = "Earth"
        expected = "5\r\nEarth\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.encode(input)
        assert result == expected

    def test_encode_empty_string(self):
        input = ""
        expected = "0\r\n\r\n"
        result = ChunkedCodingConverter.encode(input)
        assert result == expected

    def test_encode_long_string(self):
        input = "pqrstuvwxyz"
        expected = "b\r\npqrstuvwxyz\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.encode(input)
        assert result == expected

    def test_decode_valid_chunked(self):
        input = "4\r\nCode\r\n3\r\nGen\r\n0\r\n\r\n"
        expected = "CodeGen"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_decode_empty_chunked(self):
        input = "0\r\n\r\n"
        expected = ""
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_decode_invalid_hex(self):
        input = "QR\r\nfail\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.decode(input)
        assert result is None

    def test_decode_missing_crlf_after_chunk_data(self):
        input = "6\r\nplanet5\r\nEarth\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.decode(input)
        assert result is None

    def test_decode_chunk_with_extensions(self):
        input = "2;xy\r\nHi\r\n3;test\r\nSun\r\n0\r\n\r\n"
        expected = "HiSun"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_decode_extra_crlf_between_chunks(self):
        input = "1\r\ne\r\n\r\n2\r\nok\r\n0\r\n\r\n"
        expected = "eok"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_decode_with_spaces_in_chunk_ext(self):
        input = "4 ;a\r\nJava\r\n5\r\nTests\r\n0\r\n\r\n"
        expected = "JavaTests"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_decode_with_different_chunk_sizes(self):
        input = "3\r\nbye\r\n1\r\n!\r\n2\r\nok\r\n0\r\n\r\n"
        expected = "bye!ok"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_decode_nonascii(self):
        input = "2\r\nαβ\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.decode(input)
        assert result is None

    def test_encode_unicode(self):
        input = "测试"
        expected = "6\r\n测试\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.encode(input)
        assert result == expected

    def test_decode_capital_hex(self):
        input = "B\r\n12345678901\r\n0\r\n\r\n"
        expected = "12345678901"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_decode_lowercase_hex(self):
        input = "9\r\nchunkdata\r\n0\r\n\r\n"
        expected = "chunkdata"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_encode_capital_and_lowercase(self):
        input = "GenAI"
        expected = "5\r\nGenAI\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.encode(input)
        assert result == expected

    def test_decode_single_chunk(self):
        input = "4\r\nabcd\r\n0\r\n\r\n"
        expected = "abcd"
        result = ChunkedCodingConverter.decode(input)
        assert result == expected

    def test_encode_multibyte_character(self):
        input = "ø"
        expected = "2\r\nø\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.encode(input)
        assert result == expected

    def test_decode_utf8(self):
        input = "2\r\nλμ\r\n0\r\n\r\n"
        result = ChunkedCodingConverter.decode(input)
        assert result is None

    def test_decode_trailing_characters_after_last_chunk(self):
        input = "3\r\nxyz\r\n0\r\n\ntail"
        result = ChunkedCodingConverter.decode(input)
        assert result is None
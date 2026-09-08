import pytest

try:
    import buffer_crc32 as crc32
except ImportError:
    class FakeCRC32:
        @staticmethod
        def __call__(input, partial=None):
            raise NotImplementedError("Implement buffer_crc32 before running tests")

        @staticmethod
        def signed(input, partial=None):
            raise NotImplementedError("Implement buffer_crc32.signed before running tests")
        
        @staticmethod
        def unsigned(input, partial=None):
            raise NotImplementedError("Implement buffer_crc32.unsigned before running tests")
    crc32 = FakeCRC32()

def test_crc32_different_string_public():
    input_data = b'hello world'
    expected = bytes([0x1c, 0x29, 0x7d, 0x87])
    assert crc32(input_data) == expected

def test_another_short_string_public():
    input_data = b'DATA'
    expected = bytes([0x8d, 0xe5, 0x8c, 0x46])
    assert crc32(input_data) == expected

def test_byte_array_different_values_public():
    input_data = bytes([0x01, 0x02, 0x03, 0x04])
    expected = bytes([0xb1, 0x67, 0x9e, 0xd6])
    assert crc32(input_data) == expected

def test_crc32_of_utf8_string_public():
    input_data = '测试'.encode('utf-8')
    expected = bytes([0x91, 0xca, 0xd8, 0xeb])
    assert crc32(input_data) == expected

def test_casts_to_buffer_for_utf8_string_public():
    input_data = '测试'
    expected = bytes([0x91, 0xca, 0xd8, 0xeb])
    assert crc32(input_data) == expected

def test_signed_value_different_input_public():
    input_data = 'grilled cheese'
    expected = -1929599608
    assert crc32.signed(input_data) == expected

def test_unsigned_value_different_input_public():
    input_data = 'turkey sandwich'
    expected = 1477935989
    assert crc32.unsigned(input_data) == expected

def test_crc32_append_mode_alternate_strings_public():
    input_buffers = [b'foo', b' ', b'bar', b' ', b'baz']
    expected = bytes([0x25, 0x4b, 0xa2, 0x5d])
    crc = 0
    for part in input_buffers:
        crc = crc32(part, crc)
    assert crc == expected

def test_signed_in_append_mode_alternate_public():
    input1 = 'grilled'
    input2 = ' '
    input3 = 'cheese'
    expected = -1929599608

    crc = crc32.signed(input1)
    crc = crc32.signed(input2, crc)
    crc = crc32.signed(input3, crc)
    assert crc == expected

def test_accepts_integer_as_input_public():
    try:
        result = crc32(12345)
        assert result == bytes([0x00, 0x00, 0x30, 0x39])
    except Exception:
        pytest.fail("should be able to accept integer")

def test_throws_on_array_input_public():
    with pytest.raises(Exception):
        crc32([])

def test_unsigned_in_append_mode_alternate_public():
    input1 = 'turkey sand'
    input2 = 'wich'
    expected = 1477935989

    crc = crc32.unsigned(input1)
    crc = crc32.unsigned(input2, crc)
    assert crc == expected
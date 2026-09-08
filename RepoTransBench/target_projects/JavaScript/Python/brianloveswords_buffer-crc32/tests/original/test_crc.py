import pytest

# If you re-implement buffer_crc32 in Python, import it; for now, use a placeholder
import sys
import types

# Placeholder - Replace with real implementation!
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


def test_simple_crc32_is_no_problem():
    input_data = b'hey sup bros'
    expected = bytes([0x47, 0xfa, 0x55, 0x70])
    assert crc32(input_data) == expected

def test_another_simple_one():
    input_data = b'IEND'
    expected = bytes([0xae, 0x42, 0x60, 0x82])
    assert crc32(input_data) == expected

def test_slightly_more_complex():
    input_data = bytes([0x00, 0x00, 0x00])
    expected = bytes([0xff, 0x41, 0xd9, 0x12])
    assert crc32(input_data) == expected

def test_complex_crc32_gets_calculated_like_a_champ():
    input_data = 'शीर्षक'.encode('utf-8')
    expected = bytes([0x17, 0xb8, 0xaf, 0xf1])
    assert crc32(input_data) == expected

def test_casts_to_buffer_if_necessary():
    input_data = 'शीर्षक'
    expected = bytes([0x17, 0xb8, 0xaf, 0xf1])
    assert crc32(input_data) == expected

def test_can_do_signed():
    input_data = 'ham sandwich'
    expected = -1891873021
    assert crc32.signed(input_data) == expected

def test_can_do_unsigned():
    input_data = 'bear sandwich'
    expected = 3711466352
    assert crc32.unsigned(input_data) == expected

def test_simple_crc32_in_append_mode():
    input_buffers = [
        b'hey',
        b' ',
        b'sup',
        b' ',
        b'bros'
    ]
    expected = bytes([0x47, 0xfa, 0x55, 0x70])
    crc = 0
    for part in input_buffers:
        crc = crc32(part, crc)
    assert crc == expected

def test_can_do_signed_in_append_mode():
    input1 = 'ham'
    input2 = ' '
    input3 = 'sandwich'
    expected = -1891873021

    crc = crc32.signed(input1)
    crc = crc32.signed(input2, crc)
    crc = crc32.signed(input3, crc)
    assert crc == expected

def test_crc32_can_accept_integer_as_first_arg():
    try:
        result = crc32(0)
        assert result == bytes([0x00, 0x00, 0x00, 0x00])
    except Exception:
        pytest.fail('should be able to accept integer')

def test_crc32_throws_on_bad_input():
    with pytest.raises(Exception):
        crc32({})

def test_can_do_unsigned_in_append_mode():
    input1 = 'bear san'
    input2 = 'dwich'
    expected = 3711466352

    crc = crc32.unsigned(input1)
    crc = crc32.unsigned(input2, crc)
    assert crc == expected
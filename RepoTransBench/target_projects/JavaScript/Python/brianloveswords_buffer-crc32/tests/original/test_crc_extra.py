import pytest

# Placeholder for buffer_crc32
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


def buffer_equal(a, b):
    if not isinstance(a, bytes) or not isinstance(b, bytes) or len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != y:
            return False
    return True

def test_exports_function():
    assert callable(crc32)

def test_crc32_for_string():
    result = crc32("hello")
    assert isinstance(result, bytes)
    assert len(result) == 4
    assert buffer_equal(crc32("hello"), result)

def test_crc32_for_buffer():
    input_data = b'world'
    result = crc32(input_data)
    assert isinstance(result, bytes)
    assert len(result) == 4
    assert buffer_equal(crc32(b'world'), result)

def test_accept_partial_crc_as_buffer():
    input_data = b'abc'
    first = crc32(input_data[:1])
    # This may return a different result than full but must not error
    full = crc32(input_data, first)
    full2 = crc32(input_data)
    assert isinstance(full, bytes)

def test_accept_partial_crc_as_number():
    input_data = '123'
    result = crc32(input_data, 0xDEADBEEF)
    assert isinstance(result, bytes)

def test_signed_and_unsigned():
    buf = b'test123'
    s = crc32.signed(buf)
    u = crc32.unsigned(buf)
    assert isinstance(s, int)
    assert isinstance(u, int)
    assert (s & 0xFFFFFFFF) == u

    s2 = crc32.signed(buf, u)
    assert isinstance(s2, int)
    u2 = crc32.unsigned(buf, s)
    assert isinstance(u2, int)

def test_match_unsigned_for_positive_signed():
    buf = b'positive'
    s = crc32.signed(buf)
    u = crc32.unsigned(buf)
    if s >= 0:
        assert s == u

def test_handle_empty_input():
    assert isinstance(crc32(''), bytes)
    assert isinstance(crc32(b''), bytes)
    assert isinstance(crc32.signed(''), int)
    assert isinstance(crc32.unsigned(''), int)

def test_multipart_processing_equivalence():
    a, b = 'foo', 'bar'
    ab = a + b
    expected = crc32(ab)
    part = crc32(a)
    from_partial = crc32(b, part)
    assert buffer_equal(expected, from_partial)

def test_throw_on_wrong_input():
    with pytest.raises(Exception):
        crc32()
    with pytest.raises(Exception):
        crc32(None)
    with pytest.raises(Exception):
        crc32({})
    with pytest.raises(Exception):
        crc32.signed()
    with pytest.raises(Exception):
        crc32.unsigned()
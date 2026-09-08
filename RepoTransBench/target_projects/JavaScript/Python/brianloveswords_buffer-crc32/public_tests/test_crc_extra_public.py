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

def buffer_equal(a, b):
    if not isinstance(a, bytes) or not isinstance(b, bytes) or len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != y:
            return False
    return True

def test_export_function_public():
    assert callable(crc32)

def test_crc32_different_string():
    result = crc32("bye")
    assert isinstance(result, bytes)
    assert len(result) == 4
    assert buffer_equal(crc32("bye"), result)

def test_crc32_different_buffer():
    input_data = b'moon'
    result = crc32(input_data)
    assert isinstance(result, bytes)
    assert len(result) == 4
    assert buffer_equal(crc32(b'moon'), result)

def test_accept_partial_crc_as_buffer_public():
    input_data = b'xyz'
    first = crc32(input_data[:1])
    full = crc32(input_data, first)
    full2 = crc32(input_data)
    assert isinstance(full, bytes)

def test_accept_partial_crc_as_number_public():
    input_data = '789'
    result = crc32(input_data, 0xABCDEF00)
    assert isinstance(result, bytes)

def test_compute_signed_unsigned_public():
    buf = b'alpha'
    s = crc32.signed(buf)
    u = crc32.unsigned(buf)
    assert isinstance(s, int)
    assert isinstance(u, int)
    assert (s & 0xFFFFFFFF) == u

    s2 = crc32.signed(buf, u)
    assert isinstance(s2, int)
    u2 = crc32.unsigned(buf, s)
    assert isinstance(u2, int)

def test_match_unsigned_positive_public():
    buf = b'beta'
    s = crc32.signed(buf)
    u = crc32.unsigned(buf)
    if s >= 0:
        assert s == u

def test_handle_empty_input_public():
    assert isinstance(crc32(''), bytes)
    assert isinstance(crc32(b''), bytes)
    assert isinstance(crc32.signed(''), int)
    assert isinstance(crc32.unsigned(''), int)

def test_multpart_equivalent_public():
    a, b = 'ping', 'pong'
    ab = a + b
    expected = crc32(ab)
    part = crc32(a)
    from_partial = crc32(b, part)
    assert buffer_equal(expected, from_partial)

def test_throw_on_wrong_input_public():
    with pytest.raises(Exception):
        crc32()
    with pytest.raises(Exception):
        crc32(None)
    with pytest.raises(Exception):
        crc32()
    with pytest.raises(Exception):
        crc32.signed()
    with pytest.raises(Exception):
        crc32.unsigned()
import pytest

class H264Decoder:
    def __init__(self):
        self._reset_called = False

    def decode(self, data, length):
        if data is None:
            return False
        if not hasattr(data, '__iter__'):
            return False
        if length == 0:
            return False
        # For this simulation, we always return False as in C++ tests
        return False

    def reset(self):
        self._reset_called = True

def test_simple_decode_null():
    decoder = H264Decoder()
    assert not decoder.decode(None, 0)

def test_simple_decode_empty_input():
    decoder = H264Decoder()
    empty = []
    assert not decoder.decode(empty, 0)

def test_sequence_decode():
    decoder = H264Decoder()
    fake_data = [0, 1, 2, 3, 4, 5, 6, 7]
    assert not decoder.decode(fake_data, 8)

def test_reset_functionality():
    decoder = H264Decoder()
    decoder.reset()
    copy_data = [10, 20, 30, 40]
    assert not decoder.decode(copy_data, 4)
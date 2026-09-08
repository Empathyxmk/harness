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
        # For this simulation, always return False
        return False

    def reset(self):
        self._reset_called = True

def test_decode_null_changed():
    decoder = H264Decoder()
    assert not decoder.decode(None, 13)

def test_decode_zero_length_input():
    decoder = H264Decoder()
    nothing = [0x00]
    assert not decoder.decode(nothing, 0)

def test_sequence_decode_different_input():
    decoder = H264Decoder()
    new_fake = [42, 9, 10, 22, 17, 8]
    assert not decoder.decode(new_fake, 6)

def test_reset_still_fails_with_other_data():
    decoder = H264Decoder()
    decoder.reset()
    another_data = [9, 7, 4, 1, 0]
    assert not decoder.decode(another_data, 5)
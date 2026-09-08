import pytest

# Reuse the JpegqsControl class as its definition is identical
class JpegqsControl:
    """
    Minimal jpegqs_control_t struct equivalent for testing purposes.
    """
    def __init__(self):
        self.flags = 0
        self.quality = 0
        self.iter = 0

def test_jpegqs_control_nondefault():
    """
    Test for non-default values of JpegqsControl.
    Corresponds to START_TEST(test_jpegqs_control_nondefault) in C.
    """
    opts = JpegqsControl()
    opts.flags = 1
    opts.quality = 85
    opts.iter = 2
    assert opts.flags == 1
    assert opts.quality == 85
    assert opts.iter == 2

def test_jpegqs_control_reset():
    """
    Test resetting JpegqsControl to default zero.
    Corresponds to START_TEST(test_jpegqs_control_reset) in C.
    Simulates memset(&opts, 0xAA, sizeof(opts)); then memset(&opts, 0, sizeof(opts));
    """
    opts = JpegqsControl()
    # Simulate setting to 0xAA (non-zero) - Python objects don't work like raw memory
    opts.flags = 0xAAAAAAAA # Effectively non-zero
    opts.quality = 0xAAAAAA
    opts.iter = 0xAAAAAA

    # Simulate memset to 0
    # In Python, this means re-initializing or manually setting to zero
    opts.flags = 0
    opts.quality = 0
    opts.iter = 0

    assert opts.flags == 0
    assert opts.quality == 0
    assert opts.iter == 0
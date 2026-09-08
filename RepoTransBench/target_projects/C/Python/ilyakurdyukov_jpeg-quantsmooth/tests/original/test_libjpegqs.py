import pytest

class JpegqsControl:
    """
    Minimal jpegqs_control_t struct equivalent for testing purposes.
    """
    def __init__(self):
        self.flags = 0
        self.quality = 0
        self.iter = 0

def test_jpegqs_control_default():
    """
    Test for default values of JpegqsControl.
    Corresponds to START_TEST(test_jpegqs_control_default) in C.
    """
    opts = JpegqsControl()
    assert opts.flags == 0
    assert opts.quality == 0
    assert opts.iter == 0

# Note: In C, main and suite_create are part of Check framework setup.
# With pytest, test functions are automatically discovered and run.
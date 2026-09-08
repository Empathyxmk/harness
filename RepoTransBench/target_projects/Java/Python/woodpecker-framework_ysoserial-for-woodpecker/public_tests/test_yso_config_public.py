# Translated from YsoConfigPublicTest.java

class YsoConfig:
    def __init__(self):
        self._compress = False
    def is_compress(self):
        return self._compress
    def set_compress(self, value):
        self._compress = value

def test_compress_flag_toggle():
    config = YsoConfig()
    assert config.is_compress() is False
    config.set_compress(True)
    assert config.is_compress() is True
    config.set_compress(False)
    assert config.is_compress() is False

def test_multiple_toggles():
    config = YsoConfig()
    config.set_compress(True)
    config.set_compress(True)
    assert config.is_compress() is True
    config.set_compress(False)
    assert config.is_compress() is False
    config.set_compress(True)
    assert config.is_compress() is True
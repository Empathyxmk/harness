# Translated from YsoConfigTest.java

class YsoConfig:
    def __init__(self):
        self._compress = False
    def is_compress(self):
        return self._compress
    def set_compress(self, val):
        self._compress = val

def test_default_is_compress_is_false():
    config = YsoConfig()
    assert not config.is_compress()

def test_set_compress_true():
    config = YsoConfig()
    config.set_compress(True)
    assert config.is_compress()

def test_set_compress_false():
    config = YsoConfig()
    config.set_compress(True)
    config.set_compress(False)
    assert not config.is_compress()
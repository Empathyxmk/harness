# Translated from YsoConfigSmokePublicTest.java

class YsoConfig:
    def __init__(self):
        self._compress = False
    def is_compress(self):
        return self._compress
    def set_compress(self, value):
        self._compress = value

def test_default_compress_flag():
    config = YsoConfig()
    assert config.is_compress() is False

def test_set_compress_to_true():
    config = YsoConfig()
    config.set_compress(True)
    assert config.is_compress() is True

def test_set_compress_to_false():
    config = YsoConfig()
    config.set_compress(True)
    config.set_compress(False)
    assert config.is_compress() is False
# Translated from GeneratePayloadPublicTest.java

class YsoConfig:
    def __init__(self):
        self._compress = False
    def set_compress(self, value):
        self._compress = value
    def is_compress(self):
        return self._compress

class GeneratePayload:
    yso_config = YsoConfig()

def test_yso_config_compress():
    GeneratePayload.yso_config.set_compress(True)
    assert GeneratePayload.yso_config.is_compress() is True
    GeneratePayload.yso_config.set_compress(False)
    assert GeneratePayload.yso_config.is_compress() is False
    GeneratePayload.yso_config.set_compress(True)
    assert GeneratePayload.yso_config.is_compress() is True
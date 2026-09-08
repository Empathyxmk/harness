# Translated from YsoConfigSmokeTest.java

class YsoConfig:
    def __init__(self):
        self._config = {}
    def get_config(self):
        return self._config
    def set_config(self, config):
        self._config = config
    def __str__(self):
        return str(self._config)

def test_default_config():
    conf = YsoConfig()
    assert conf is not None
    assert conf.get_config() is not None

def test_set_and_get_config():
    conf = YsoConfig()
    props = {"foo": "bar"}
    conf.set_config(props)
    assert conf.get_config()["foo"] == "bar"

def test_to_string():
    conf = YsoConfig()
    conf.get_config()["k"] = "v"
    text_repr = str(conf)
    assert "k" in text_repr
    assert "v" in text_repr
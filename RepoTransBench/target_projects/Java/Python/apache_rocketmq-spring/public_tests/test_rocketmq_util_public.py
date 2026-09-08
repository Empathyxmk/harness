def test_default_charset_constant_is_utf8_public():
    class RocketMQUtil:
        DEFAULT_CHARSET = type('Charset', (), {'name': lambda: "UTF-8"})()
    assert RocketMQUtil.DEFAULT_CHARSET.name() == "UTF-8"
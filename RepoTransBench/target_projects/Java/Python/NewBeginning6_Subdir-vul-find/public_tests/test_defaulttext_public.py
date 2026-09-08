class DefaultText:
    @staticmethod
    def getDefault():
        return "Default text, some long value"

def test_get_default():
    text = DefaultText.getDefault()
    assert text is not None
    assert "text" in text or len(text) > 10
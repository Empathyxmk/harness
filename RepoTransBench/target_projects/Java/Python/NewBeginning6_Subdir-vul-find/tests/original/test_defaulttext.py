class DefaultText:
    @staticmethod
    def getDefault():
        return "Default Text Value"

def test_get_default():
    val = DefaultText.getDefault()
    assert val is not None
    assert val != ""
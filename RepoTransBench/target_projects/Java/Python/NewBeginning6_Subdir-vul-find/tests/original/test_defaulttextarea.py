class DefaultTextarea:
    @staticmethod
    def getDefault():
        return "Default Textarea Value"

def test_get_default():
    val = DefaultTextarea.getDefault()
    assert val is not None
    assert val != ""
class DefaultTextarea:
    @staticmethod
    def getDefault():
        return "   something here\n   "

def test_get_default():
    val = DefaultTextarea.getDefault()
    assert val is not None
    assert len(val.strip()) > 0
import betterprompt

def test_all_exports():
    for name in betterprompt.__all__:
        assert hasattr(betterprompt, name)
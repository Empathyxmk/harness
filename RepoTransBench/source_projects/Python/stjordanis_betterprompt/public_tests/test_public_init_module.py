import betterprompt

def test_public_all_exports():
    # Test the same logic but interact via __dict__ as well
    for name in betterprompt.__all__:
        assert name in betterprompt.__dict__
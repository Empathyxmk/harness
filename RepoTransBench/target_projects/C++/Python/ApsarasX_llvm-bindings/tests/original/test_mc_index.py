import pytest

# Dummy MCIndex for demonstration purposes
class MCIndex:
    def __init__(self, idx):
        self.idx = idx

    def get_index(self):
        return self.idx

def test_mcindex_get_correct_index():
    m = MCIndex(42)
    assert m.get_index() == 42
    n = MCIndex(-19)
    assert n.get_index() == -19
import pytest

# Dummy MCIndex for demonstration purposes (public test)
class MCIndex:
    def __init__(self, idx):
        self.idx = idx

    def get_index(self):
        return self.idx

def test_mcindex_get_correct_index_public():
    x = MCIndex(101)
    assert x.get_index() == 101
    y = MCIndex(-202)
    assert y.get_index() == -202
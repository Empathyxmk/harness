import pytest

class CreateChunkDialog:
    def __init__(self):
        self._name = ""
        self._size = 0

    def set_chunk_name(self, name):
        self._name = name

    def chunk_name(self):
        return self._name

    def set_chunk_size(self, size):
        self._size = size

    def chunk_size(self):
        return self._size

def test_dialog_has_different_chunk_name():
    dialog = CreateChunkDialog()
    dialog.set_chunk_name("the_public_chunk")
    assert dialog.chunk_name() == "the_public_chunk"

def test_chunk_size_is_correct():
    dialog = CreateChunkDialog()
    dialog.set_chunk_size(123456)
    assert dialog.chunk_size() == 123456
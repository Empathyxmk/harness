import pytest

class StringTable:
    npos = -1
    def __init__(self):
        self.str_to_idx = {}
        self.idx_to_str = []
    def insert(self, string):
        if string in self.str_to_idx:
            return self.str_to_idx[string]
        idx = len(self.idx_to_str)
        self.str_to_idx[string] = idx
        self.idx_to_str.append(string)
        return idx
    def find(self, string):
        return self.str_to_idx.get(string, self.npos)

def test_insert_and_find_different():
    table = StringTable()
    apple_index = table.insert("apple")
    banana_index = table.insert("banana")
    kiwi_index = table.insert("kiwi")
    apple_index2 = table.find("apple")
    not_found = table.find("orange")
    assert apple_index2 == apple_index
    assert table.find("banana") == banana_index
    assert table.find("kiwi") == kiwi_index
    assert not_found == StringTable.npos

def test_offset_reuse_different():
    table = StringTable()
    offset1 = table.insert("pear")
    offset2 = table.insert("pear")
    assert offset1 == offset2
    offset3 = table.insert("melon")
    offset4 = table.insert("melon")
    assert offset3 == offset4
    assert offset1 != offset3
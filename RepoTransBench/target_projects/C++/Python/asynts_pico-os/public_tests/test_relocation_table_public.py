import pytest

class MockStringTable:
    npos = -1
    # For compliance

class MockElfRel:
    def __init__(self, r_offset, r_info):
        self.r_offset = r_offset
        self.r_info = r_info

class RelocationTable:
    def __init__(self, string_table, name, entry_size, type_):
        self.entries = []
    def add_entry(self, rel):
        self.entries.append(rel)
    def size(self):
        return len(self.entries)
    def get(self, idx):
        return self.entries[idx]

def test_add_entry_different():
    string_table = MockStringTable()
    reloc_table = RelocationTable(string_table, ".reltest", 8, 1)
    rel1 = MockElfRel(200, 0x12345)
    rel2 = MockElfRel(300, 0x67890)
    reloc_table.add_entry(rel1)
    reloc_table.add_entry(rel2)
    assert reloc_table.size() == 2
    assert reloc_table.get(0).r_offset == 200
    assert reloc_table.get(1).r_offset == 300

def test_empty_table_different():
    string_table = MockStringTable()
    reloc_table = RelocationTable(string_table, ".reltest.empty", 5, 4)
    assert reloc_table.size() == 0
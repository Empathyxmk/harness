import pytest

class Table:
    def __init__(self):
        self.columns = []
        self._open = True
        self._rows = []
    def addColumn(self, col):
        if not self._open:
            raise RuntimeError("Can't add column.")
        self.columns.append(col)
    def addRow(self, row):
        if not self.columns:
            raise RuntimeError("Must add columns before adding rows")
        if len(row) != len(self.columns):
            raise IndexError("Row length does not match column count")
        self._rows.append(list(row))
        self._open = False
    def hashes(self):
        return [dict(zip(self.columns, row)) for row in self._rows]

def test_forbids_rows_not_matching_table_columns_size():
    t = Table()
    t.addColumn("C1")
    with pytest.raises(IndexError):
        t.addRow([])
    t.addRow(["R1"])
    with pytest.raises(IndexError):
        t.addRow(["R1", "R2"])

def test_rows_cannot_be_added_before_columns_are_set():
    t = Table()
    with pytest.raises(RuntimeError):
        t.addRow([])

def test_columns_cannot_be_changes_after_rows_are_added():
    t = Table()
    t.addColumn("C1")
    t.addRow(["R1"])
    with pytest.raises(RuntimeError):
        t.addColumn("C2")

def test_added_rows_match_column_definition():
    t = Table()
    t.addColumn("C1")
    t.addColumn("C2")
    t.addColumn("C3")
    assert len(t.hashes()) == 0

    t.addRow(["R11", "R12", "R13"])
    hashes = t.hashes()
    assert len(hashes) == 1
    assert hashes[0]["C1"] == "R11"
    assert hashes[0]["C2"] == "R12"
    assert hashes[0]["C3"] == "R13"

    t.addRow(["R21", "R22", "R23"])
    t.addRow(["R31", "R32", "R33"])
    t.addRow(["R41", "R42", "R43"])
    hashes = t.hashes()
    assert len(hashes) == 4
    assert hashes[1]["C1"] == "R21"
    assert hashes[2]["C2"] == "R32"
    assert hashes[3]["C3"] == "R43"
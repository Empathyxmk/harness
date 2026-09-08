import os
import tempfile

class Mapping:
    def __init__(self, file_path=None):
        self._map = {}
        if file_path is None:
            return
        if not os.path.exists(file_path):
            return
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                if "->" in line:
                    parts = line.split("->")
                    if len(parts) == 2:
                        left, right = parts
                        # Ignore trailing colon on right
                        self._map[left.strip()] = right.strip().rstrip(":")
                # Otherwise ignore malformed lines

    def get(self, class_name):
        return self._map.get(class_name)

    def get_mapping(self):
        return self._map

def test_valid_mappings(tmp_path):
    mapping_file = tmp_path / "mapping.txt"
    mapping_file.write_text(
        "# This is a comment\n"
        "com.abc.ClassA -> com.obf.X:\n"
        "  # Indented comment\n"
        "com.abc.ClassB -> com.obf.Y:\n"
        "bad mapping line\n"
        "com.abc.ClassC -> com.obf.Z:\n"
    )
    mapping = Mapping(str(mapping_file))
    assert mapping.get("com.abc.ClassA") == "com.obf.X"
    assert mapping.get("com.abc.ClassB") == "com.obf.Y"
    assert mapping.get("com.abc.ClassC") == "com.obf.Z"
    assert mapping.get("com.abc.NotExist") is None
    assert len(mapping.get_mapping()) >= 3

def test_null_file():
    m = Mapping(None)
    assert m.get_mapping() == {}

def test_non_existent_file():
    m = Mapping("fakefile_doesnot_exist.txt")
    assert m.get_mapping() == {}

def test_malformed_lines(tmp_path):
    malformed_file = tmp_path / "malformed.txt"
    malformed_file.write_text(
        "malformed_line\n"
        "com.onlyonepart -> \n"
        " -> onlysecondpart:\n"
        "correct.package -> correct.target:\n"
    )
    m = Mapping(str(malformed_file))
    assert m.get("correct.package") == "correct.target"
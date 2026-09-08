import pytest
import os

# --- Begin: Minimal INI File class to simulate needed test functionality ---

class CIniFile:
    def __init__(self, filename=None):
        # Simulate protected member variables from C++
        self.m_bLastResult = False
        self.m_bModified = False
        self.m_bReadOnly = False
        self._data = {}
        if filename is not None:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    section = None
                    for line in f:
                        line = line.strip()
                        if line.startswith('[') and line.endswith(']'):
                            section = line[1:-1]
                        elif '=' in line and section is not None:
                            k, v = line.split('=', 1)
                            self._data.setdefault(section, {})[k.strip()] = v.strip()
                self.m_bLastResult = True
            except Exception:
                self.m_bLastResult = False

    # Simulate SetString and SetInt methods
    def SetString(self, section, key, value):
        self.m_bModified = True
        if section not in self._data:
            self._data[section] = {}
        self._data[section][key] = value

    def SetInt(self, section, key, value):
        self.SetString(section, key, str(value))

    def GetFileString(self, section, key):
        try:
            return self._data[section][key]
        except KeyError:
            return ""

    def GetString(self, section, key):
        try:
            return self._data[section][key]
        except KeyError:
            return ""

    def GetInt(self, section, key):
        try:
            return int(self._data[section][key])
        except (KeyError, ValueError):
            return 0

# Test subclass (for friends/protected access in the C++ code, not strictly needed in Python)
CIniFile_Friend = CIniFile
# --- End: Minimal implementation ---

def test_constructor_default():
    ini = CIniFile_Friend()
    assert not ini.m_bLastResult
    assert not ini.m_bModified
    assert not ini.m_bReadOnly

def test_constructor_load_file(tmp_path):
    ini_file = tmp_path / "test.ini"
    ini_file.write_text("[TEST]\nfoo=bar\n", encoding="utf-8")
    ini = CIniFile_Friend(str(ini_file))
    assert ini.GetFileString("TEST", "foo") == "bar"
    # File is auto cleaned up by tmp_path

def test_set_and_get_string():
    ini = CIniFile_Friend()
    ini.SetString("Section", "Key", "Value")
    assert ini.GetString("Section", "Key") == "Value"

def test_set_and_get_int():
    ini = CIniFile_Friend()
    ini.SetInt("Numbers", "Number", 123)
    assert ini.GetInt("Numbers", "Number") == 123
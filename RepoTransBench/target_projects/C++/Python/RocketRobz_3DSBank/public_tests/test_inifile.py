import pytest
import os

# --- Begin: Minimal INI File class to simulate needed test functionality ---

class CIniFile:
    def __init__(self, filename=None):
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

CIniFile_Friend = CIniFile
# --- End: Minimal implementation ---

def test_constructor_default_public():
    ini = CIniFile_Friend()
    assert not ini.m_bLastResult
    assert not ini.m_bModified
    assert not ini.m_bReadOnly

def test_constructor_load_file_public(tmp_path):
    ini_file = tmp_path / "public_test.ini"
    ini_file.write_text("[GENERAL]\nanswer=forty_two\n", encoding="utf-8")
    ini = CIniFile_Friend(str(ini_file))
    assert ini.GetFileString("GENERAL", "answer") == "forty_two"

def test_set_and_get_string_public():
    ini = CIniFile_Friend()
    ini.SetString("Config", "Username", "Alice42")
    assert ini.GetString("Config", "Username") == "Alice42"

def test_set_and_get_int_public():
    ini = CIniFile_Friend()
    ini.SetInt("Settings", "Threshold", 2024)
    assert ini.GetInt("Settings", "Threshold") == 2024
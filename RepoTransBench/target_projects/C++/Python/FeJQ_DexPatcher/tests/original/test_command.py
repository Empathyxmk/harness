import pytest
import sys
from io import StringIO

# --- Minimal stubs based on mock C++ test environment ---

class Parser:
    mock_version = False
    mock_fix = False
    mock_dex_path = False
    mock_json_path = False
    mock_nolog = False
    mock_dex_path_value = "dex.dex"
    mock_json_path_value = "info.json"
    called_usage = False

    @classmethod
    def reset(cls):
        cls.mock_version = False
        cls.mock_fix = False
        cls.mock_dex_path = False
        cls.mock_json_path = False
        cls.mock_nolog = False
        cls.mock_dex_path_value = "dex.dex"
        cls.mock_json_path_value = "info.json"
        cls.called_usage = False

    def __init__(self):
        pass

    def add(self, *args, **kwargs):
        pass

    def set_program_name(self, name):
        pass

    def parse_check(self, argc, argv):
        pass

    def exist(self, key):
        if key == "version" and self.mock_version:
            return True
        if key == "fix" and self.mock_fix:
            return True
        if key == "dex-path" and self.mock_dex_path:
            return True
        if key == "json-path" and self.mock_json_path:
            return True
        if key == "nolog" and self.mock_nolog:
            return True
        return False

    def get(self, key):
        if key == "dex-path":
            return self.mock_dex_path_value
        if key == "json-path":
            return self.mock_json_path_value
        return None

    def usage(self):
        self.called_usage = True
        Parser.called_usage = True


class ParseDex:
    def __init__(self, path):
        self.path = path
    def fixMethod(self, info, nolog):
        pass


class PatchDex(ParseDex):
    lastInstance = None
    def __init__(self, p):
        super().__init__(p)
        self.fixedMagicPath = p
        self.fixedMethodDexPath = ""
        self.fixedMethodJsonPath = ""
        self.fixedMagicCalled = False
        self.fixedMethodCalled = False
        self.nolog = False
        PatchDex.lastInstance = self

    def fixDexMagic(self, flag):
        self.fixedMagicCalled = flag

    def fixMethod(self, info, noLog):
        self.fixedMethodDexPath = self.fixedMagicPath
        self.fixedMethodJsonPath = info
        self.nolog = noLog
        self.fixedMethodCalled = True


class Build:
    @staticmethod
    def GetBuildDate():
        return "2024-01-01"

# --- The Command class (stub implementation for tests) ---
class Command:
    def __init__(self):
        pass

    def initHandler(self, argc, argv):
        # Mocks the C++ CLI handler logic; adapts the logic for test stimulations.
        parser = Parser()
        parser.mock_version = Parser.mock_version
        parser.mock_fix = Parser.mock_fix
        parser.mock_dex_path = Parser.mock_dex_path
        parser.mock_json_path = Parser.mock_json_path
        parser.mock_nolog = Parser.mock_nolog
        parser.mock_dex_path_value = Parser.mock_dex_path_value
        parser.mock_json_path_value = Parser.mock_json_path_value
        out = sys.stdout

        if parser.mock_version:
            print("DexPatcher version 1.0.0 by MockAuthor, date:", Build.GetBuildDate())
            return
        elif parser.mock_fix:
            if parser.mock_dex_path and parser.mock_json_path:
                p = PatchDex(parser.mock_dex_path_value)
                p.fixMethod(parser.mock_json_path_value, parser.mock_nolog)
                return
            elif parser.mock_dex_path:
                p = PatchDex(parser.mock_dex_path_value)
                p.fixDexMagic(True)
                return
            else:
                print("dp fix: Need --dex-path (and maybe --json-path)")
                return
        else:
            parser.usage()
            return

# --- Tests ---

def test_handles_version_option(monkeypatch, capsys):
    Parser.reset()
    Parser.mock_version = True
    cmd = Command()
    argv = ["prog", "--version"]
    cmd.initHandler(len(argv), argv)
    out = capsys.readouterr().out
    assert "DexPatcher version" in out

def test_handles_fix_method_with_json():
    Parser.reset()
    Parser.mock_fix = True
    Parser.mock_dex_path = True
    Parser.mock_json_path = True
    Parser.mock_dex_path_value = "dex.dex"
    Parser.mock_json_path_value = "info.json"
    cmd = Command()
    PatchDex.lastInstance = None
    argv = ["prog", "--fix", "--dex-path", "dex.dex", "--json-path", "info.json"]
    cmd.initHandler(len(argv), argv)
    assert PatchDex.lastInstance is not None
    p = PatchDex.lastInstance
    assert p.fixedMethodCalled
    assert p.fixedMethodDexPath == "dex.dex"
    assert p.fixedMethodJsonPath == "info.json"

def test_handles_fix_method_with_nolog():
    Parser.reset()
    Parser.mock_fix = True
    Parser.mock_dex_path = True
    Parser.mock_json_path = True
    Parser.mock_nolog = True
    Parser.mock_dex_path_value = "dex.dex"
    Parser.mock_json_path_value = "info.json"
    cmd = Command()
    PatchDex.lastInstance = None
    argv = ["prog", "--fix", "--dex-path", "dex.dex", "--json-path", "info.json", "--nolog"]
    cmd.initHandler(len(argv), argv)
    assert PatchDex.lastInstance is not None
    p = PatchDex.lastInstance
    assert p.fixedMethodCalled
    assert p.nolog

def test_handles_fix_magic():
    Parser.reset()
    Parser.mock_fix = True
    Parser.mock_dex_path = True
    Parser.mock_dex_path_value = "dex.dex"
    cmd = Command()
    PatchDex.lastInstance = None
    argv = ["prog", "--fix", "--dex-path", "dex.dex"]
    cmd.initHandler(len(argv), argv)
    assert PatchDex.lastInstance is not None
    p = PatchDex.lastInstance
    assert p.fixedMagicCalled
    assert not p.fixedMethodCalled

def test_handles_fix_no_dex_path(capsys):
    Parser.reset()
    Parser.mock_fix = True
    cmd = Command()
    argv = ["prog", "--fix"]
    cmd.initHandler(len(argv), argv)
    out = capsys.readouterr().out
    assert "dp fix" in out

def test_handles_unknown_command():
    Parser.reset()
    Parser.called_usage = False
    cmd = Command()
    argv = ["prog", "--unknown"]
    cmd.initHandler(len(argv), argv)
    assert Parser.called_usage
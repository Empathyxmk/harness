import sys
import types
import importlib
import pytest

import cemu.exports

class DummyPerm:
    def __init__(self, r, w, x): self.r, self.w, self.x = r, w, x

class DummyPESectionCharacteristics:
    MEM_READ = types.SimpleNamespace(value=1)
    MEM_WRITE = types.SimpleNamespace(value=2)
    MEM_EXECUTE = types.SimpleNamespace(value=4)
    CNT_CODE = types.SimpleNamespace(value=8)
    CNT_INITIALIZED_DATA = types.SimpleNamespace(value=16)
    CNT_UNINITIALIZED_DATA = types.SimpleNamespace(value=32)

class DummyPESectionType:
    TEXT = 1
    DATA = 2

class DummyPEHeaderChar:
    EXECUTABLE_IMAGE = 4096
    DEBUG_STRIPPED = 16384
    LARGE_ADDRESS_AWARE = 32
    NEED_32BIT_MACHINE = 256

class DummyPEOptHeader:
    DLL_CHARACTERISTICS = types.SimpleNamespace(NO_SEH=64, NX_COMPAT=256)

def dummy_PE():
    module = types.SimpleNamespace()
    module.Section = types.SimpleNamespace(CHARACTERISTICS=DummyPESectionCharacteristics)
    module.SECTION_TYPES = types.SimpleNamespace(TEXT=1, DATA=2)
    module.PE_TYPE = types.SimpleNamespace(PE32=1, PE32_PLUS=2)
    module.Header = types.SimpleNamespace(CHARACTERISTICS=DummyPEHeaderChar)
    module.OptionalHeader = DummyPEOptHeader
    cl_bin = {}
    def bin_init(self, t): cl_bin["t"] = t
    bin_cls = type("Binary", (), {
        "__init__": bin_init,
        "add_section": lambda s, sect, t: sect,
        "header": types.SimpleNamespace(
            add_characteristic=lambda x: None
        ),
        "optional_header": types.SimpleNamespace(
            addressof_entrypoint=None,
            remove=lambda x: None,
            add=lambda x: None,
            major_operating_system_version=None,
            minor_operating_system_version=None,
            major_subsystem_version=None,
            minor_subsystem_version=None,
            major_linker_version=None,
            minor_linker_version=None
        )
    })
    module.Binary = bin_cls
    class Section:
        def __init__(self, name):
            self.name = name
            self.content = None
            self.virtual_address = None
            self.characteristics = None
    module.Section = Section
    class Builder:
        def __init__(self, pe): self.pe = pe
        def build_imports(self, x): return None
        def build(self): return None
        def write(self, path):
            with open(path, "wb") as f:
                f.write(b"EXE")
    module.Builder = Builder
    return module

def test_parse_as_lief_pe_permission(monkeypatch):
    monkeypatch.setattr("cemu.exports.PE", dummy_PE())
    # r w x and various extras
    perm = DummyPerm(True, True, False)
    base = cemu.exports.parse_as_lief_pe_permission(perm)
    # MEM_READ | MEM_WRITE == 1|2 = 3
    assert base & (1|2)
    xperm = DummyPerm(True, False, True)
    val = cemu.exports.parse_as_lief_pe_permission(xperm, "code")
    assert val & 8 # CNT_CODE
    val2 = cemu.exports.parse_as_lief_pe_permission(xperm, "idata")
    assert val2 & 16
    val3 = cemu.exports.parse_as_lief_pe_permission(xperm, "udata")
    assert val3 & 32

def test_build_pe_executable(monkeypatch, tmp_path):
    pe_mod = dummy_PE()
    monkeypatch.setattr("cemu.exports.PE", pe_mod)
    # arch: only is_x86_32 or is_x86_64 may pass.
    class DummyArch: pass
    monkeypatch.setattr("cemu.exports.is_x86_32", lambda a: a == "x86")
    monkeypatch.setattr("cemu.exports.is_x86_64", lambda a: a == "x64")
    monkeypatch.setattr("cemu.exports.cemu", types.SimpleNamespace(
        utils=types.SimpleNamespace(generate_random_string=lambda x: "12345")
    ))
    sect_text = types.SimpleNamespace(
        name=".text",
        address=0x1000,
        size=0x20,
        permission=DummyPerm(True, False, True)
    )
    sect_data = types.SimpleNamespace(
        name=".data",
        address=0x2000,
        size=0x50,
        permission=DummyPerm(True, True, False)
    )
    file_out = cemu.exports.build_pe_executable(
        text=b"\xcc"*8,
        memory_layout=[sect_text, sect_data],
        arch="x86"
    )
    # Should write file to disk
    assert file_out.exists()
    # Clean-up
    file_out.unlink()

    # Test ValueError branch on unsupported arch:
    with pytest.raises(ValueError):
        cemu.exports.build_pe_executable(text=b"x", memory_layout=[sect_text], arch="arm")

def test_build_elf_executable_notimplemented():
    with pytest.raises(NotImplementedError):
        cemu.exports.build_elf_executable(b"", [], None)
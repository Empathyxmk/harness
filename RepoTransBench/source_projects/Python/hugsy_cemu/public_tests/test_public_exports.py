import sys
import types
import importlib
import pytest

import cemu.exports

class PublicDummyPerm:
    def __init__(self, r, w, x): self.r, self.w, self.x = r, w, x

class PublicDummyPESectionCharacteristics:
    MEM_READ = types.SimpleNamespace(value=10)
    MEM_WRITE = types.SimpleNamespace(value=20)
    MEM_EXECUTE = types.SimpleNamespace(value=40)
    CNT_CODE = types.SimpleNamespace(value=80)
    CNT_INITIALIZED_DATA = types.SimpleNamespace(value=160)
    CNT_UNINITIALIZED_DATA = types.SimpleNamespace(value=320)

class PublicDummyPESectionType:
    TEXT = 3
    DATA = 4

class PublicDummyPEHeaderChar:
    EXECUTABLE_IMAGE = 8888
    DEBUG_STRIPPED = 7777
    LARGE_ADDRESS_AWARE = 66
    NEED_32BIT_MACHINE = 33

class PublicDummyPEOptHeader:
    DLL_CHARACTERISTICS = types.SimpleNamespace(NO_SEH=77, NX_COMPAT=34)

def public_dummy_PE():
    module = types.SimpleNamespace()
    module.Section = types.SimpleNamespace(CHARACTERISTICS=PublicDummyPESectionCharacteristics)
    module.SECTION_TYPES = types.SimpleNamespace(TEXT=3, DATA=4)
    module.PE_TYPE = types.SimpleNamespace(PE32=7, PE32_PLUS=8)
    module.Header = types.SimpleNamespace(CHARACTERISTICS=PublicDummyPEHeaderChar)
    module.OptionalHeader = PublicDummyPEOptHeader
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
                f.write(b"PEB")
    module.Builder = Builder
    return module

def test_parse_as_lief_pe_permission_public(monkeypatch):
    monkeypatch.setattr("cemu.exports.PE", public_dummy_PE())
    perm = PublicDummyPerm(False, True, True)
    base = cemu.exports.parse_as_lief_pe_permission(perm)
    # MEM_WRITE | MEM_EXECUTE == 20|40 = 60
    assert base & (20|40)
    xperm = PublicDummyPerm(True, True, True)
    val = cemu.exports.parse_as_lief_pe_permission(xperm, "code")
    assert val & 80  # CNT_CODE
    val2 = cemu.exports.parse_as_lief_pe_permission(xperm, "idata")
    assert val2 & 160
    val3 = cemu.exports.parse_as_lief_pe_permission(xperm, "udata")
    assert val3 & 320

def test_build_pe_executable_public(monkeypatch, tmp_path):
    pe_mod = public_dummy_PE()
    monkeypatch.setattr("cemu.exports.PE", pe_mod)
    # Different arch string, only is_x86_32 or is_x86_64 may pass
    class DummyPublicArch: pass
    monkeypatch.setattr("cemu.exports.is_x86_32", lambda a: a == "i386")
    monkeypatch.setattr("cemu.exports.is_x86_64", lambda a: a == "amd64")
    monkeypatch.setattr("cemu.exports.cemu", types.SimpleNamespace(
        utils=types.SimpleNamespace(generate_random_string=lambda x: "abcdz")
    ))
    sect_text = types.SimpleNamespace(
        name=".code",
        address=0x3000,
        size=0x100,
        permission=PublicDummyPerm(False, False, True)
    )
    sect_data = types.SimpleNamespace(
        name=".vars",
        address=0x4000,
        size=0x60,
        permission=PublicDummyPerm(True, True, False)
    )
    file_out = cemu.exports.build_pe_executable(
        text=b"\x90"*16,
        memory_layout=[sect_text, sect_data],
        arch="i386"
    )
    # Should write a file to disk
    assert file_out.exists()
    with file_out.open("rb") as f:
        assert f.read(3) == b"PEB"
    file_out.unlink()

    # ValueError on unsupported arch:
    with pytest.raises(ValueError):
        cemu.exports.build_pe_executable(text=b"y", memory_layout=[sect_text], arch="armv7")

def test_build_elf_executable_notimplemented_public():
    with pytest.raises(NotImplementedError):
        cemu.exports.build_elf_executable(b"asdf", [1], "not_arch")
import string
import pytest

import cemu.core
import cemu.utils
import cemu.arch

def test_get_metadata_from_stream_public():
    raw = r"""
    ;;; @@@architecture arm
    ;;; @@@endianness big
    """
    res = cemu.utils.get_metadata_from_stream(raw)
    assert res and len(res) == 2
    assert isinstance(res[0], cemu.arch.Architecture)
    assert cemu.arch.is_arm(res[0])
    assert isinstance(res[1], cemu.arch.Endianness)
    assert res[1] == cemu.arch.Endianness.BIG_ENDIAN

def test_generate_random_string_public():
    result = cemu.utils.generate_random_string(3)
    assert len(result) == 3
    assert isinstance(result, str)
    with pytest.raises(ValueError):
        cemu.utils.generate_random_string(-2)

    res = cemu.utils.generate_random_string(20, charset=string.digits)
    assert all(c in string.digits for c in res)

def test_ishex_public():
    assert not cemu.utils.ishex("garbage")
    assert cemu.utils.ishex("abc123")
    assert not cemu.utils.ishex("hex!")
    assert not cemu.utils.ishex("xyz890")
    assert not cemu.utils.ishex("&*bad")
    assert cemu.utils.ishex("ABCDEF123456")

def test_hexdump_public():
    cemu.core.context = cemu.core.GlobalContext()
    cemu.core.context.architecture = cemu.arch.Architectures.find("mips")
    assert cemu.utils.hexdump(b"\x00\xff\x10\xee") == "0x000000  00 FF 10 EE  ...\x10\xee"
    cemu.core.context.architecture = cemu.arch.Architectures.find("arm")
    assert cemu.utils.hexdump(b"bbcc") == "0x000000  62 62 63 63  bbcc"

    with pytest.raises(ValueError):
        cemu.utils.hexdump(b"bbcc", separator="")

    assert cemu.utils.hexdump(b"\x42\x42\xbb\xaf") == "0x000000  42 42 BB AF  BB.."

    with pytest.raises(ValueError):
        cemu.utils.hexdump(b"B" * 0x11, alignment=3)

    assert cemu.utils.hexdump(b"\x42\x42\xbb\xaf", base=0x1337133713371337) == "0x1337133713371337  42 42 BB AF  BB.."
    res = cemu.utils.hexdump(b"B" * 0x10, base=0x10101010_10101010).splitlines()
    assert len(res) == 1
    assert res[0] == "0x1010101010101010  42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42  BBBBBBBBBBBBBBBB"
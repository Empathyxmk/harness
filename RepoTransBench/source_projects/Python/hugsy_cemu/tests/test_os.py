import cemu.os
import pytest

def test_operating_system_str_fspath_eq():
    linux = cemu.os.Linux
    windows = cemu.os.Windows
    # __str__ and __fspath__
    assert str(linux) == "Linux"
    assert linux.__fspath__() == "linux"
    # __eq__ with str
    assert linux == "linux"
    assert linux == "LiNUX"
    # __eq__ with object
    assert linux == cemu.os.OperatingSystem("Linux")
    assert windows != linux
    # __eq__ wrong type
    with pytest.raises(ValueError):
        linux == 42

def test_operating_system_eq_case():
    # Case-sensitive compare
    a = cemu.os.OperatingSystem("AnOS")
    b = cemu.os.OperatingSystem("AnOS")
    c = cemu.os.OperatingSystem("anotherOS")
    assert a == b
    assert not (a == c)
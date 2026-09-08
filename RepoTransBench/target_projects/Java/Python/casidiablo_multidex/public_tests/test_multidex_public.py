import pytest

class MultiDex:
    @staticmethod
    def is_vm_multidex_capable(vm_version):
        if not vm_version or not isinstance(vm_version, str):
            return False
        pieces = vm_version.strip().split(".")
        if len(pieces) < 2:
            return False
        try:
            major = int(pieces[0])
            minor = int(pieces[1])
        except Exception:
            return False
        return major > 2 or (major == 2 and minor >= 1)

def test_version_check_public():
    assert not MultiDex.is_vm_multidex_capable("0.9")
    assert not MultiDex.is_vm_multidex_capable("1.999.9999")
    assert not MultiDex.is_vm_multidex_capable("2.0.0")  # "2.0.0" should be false
    assert not MultiDex.is_vm_multidex_capable("2.0.1")  # "2.0.x" should be false

    assert MultiDex.is_vm_multidex_capable("2.10")    # 2.10 > 2.1
    assert MultiDex.is_vm_multidex_capable("2.1.1")
    assert MultiDex.is_vm_multidex_capable("4.0")
    assert MultiDex.is_vm_multidex_capable("10.2")
    assert MultiDex.is_vm_multidex_capable("2.1.1.5")
    assert MultiDex.is_vm_multidex_capable("2.2.12345")
    assert MultiDex.is_vm_multidex_capable("05.5.5")

    assert MultiDex.is_vm_multidex_capable("002.001.0001")
    assert not MultiDex.is_vm_multidex_capable("2.0.9999")
    assert not MultiDex.is_vm_multidex_capable("2.0.0000")
    assert MultiDex.is_vm_multidex_capable("3.0.42")
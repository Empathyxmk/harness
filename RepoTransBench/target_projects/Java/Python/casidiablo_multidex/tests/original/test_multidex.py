import pytest

class MultiDex:
    @staticmethod
    def is_vm_multidex_capable(vm_version):
        """
        Implements the same logic as the Java MultiDex.isVMMultidexCapable.
        - Returns True if version is >=2.1
        - The version string can be '2.1', '002.001.0001', etc.
        """
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

def test_version_check():
    assert not MultiDex.is_vm_multidex_capable(None)
    assert not MultiDex.is_vm_multidex_capable("-1.32.54")
    assert not MultiDex.is_vm_multidex_capable("1.32.54")
    assert not MultiDex.is_vm_multidex_capable("1.32")
    assert not MultiDex.is_vm_multidex_capable("2.0")
    assert not MultiDex.is_vm_multidex_capable("2.000.1254")
    assert MultiDex.is_vm_multidex_capable("2.1.1254")
    assert MultiDex.is_vm_multidex_capable("2.1")
    assert MultiDex.is_vm_multidex_capable("2.2")
    assert MultiDex.is_vm_multidex_capable("2.1.0000")
    assert MultiDex.is_vm_multidex_capable("2.2.0000")
    assert MultiDex.is_vm_multidex_capable("002.0001.0010")
    assert MultiDex.is_vm_multidex_capable("3.0")
    assert MultiDex.is_vm_multidex_capable("3.0.0")
    assert MultiDex.is_vm_multidex_capable("3.0.1")
    assert MultiDex.is_vm_multidex_capable("3.1.0")
    assert MultiDex.is_vm_multidex_capable("03.1.132645")
    assert MultiDex.is_vm_multidex_capable("03.2")
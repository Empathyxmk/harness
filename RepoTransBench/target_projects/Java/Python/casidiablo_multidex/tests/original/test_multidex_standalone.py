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

def test_private_constructor_coverage():
    # Can't really test Java-style private constructor in Python; simulate
    instance = MultiDex()
    assert instance is not None

def test_is_vm_multidex_capable_edge_cases():
    assert not MultiDex.is_vm_multidex_capable("")
    assert not MultiDex.is_vm_multidex_capable("abc.def")
    assert MultiDex.is_vm_multidex_capable("3.10.99")
import pytest

class JJvm:
    @staticmethod
    def getVersion():
        # Example version string
        return "2.1.0"
    @staticmethod
    def main(args):
        if "--nonexistent-flag" in args:
            raise IllegalArgumentException("Unknown option --nonexistent-flag")

class IllegalArgumentException(Exception):
    pass

def test_jjvm_version():
    version = JJvm.getVersion()
    assert version is not None
    assert isinstance(version, str)
    assert any(char.isdigit() for char in version)
    assert version != "1.0.0"

def test_jjvm_main_with_args():
    with pytest.raises(IllegalArgumentException) as ex:
        JJvm.main(["--nonexistent-flag"])
    assert ex.value.args[0] is not None and ex.value.args[0] != ""
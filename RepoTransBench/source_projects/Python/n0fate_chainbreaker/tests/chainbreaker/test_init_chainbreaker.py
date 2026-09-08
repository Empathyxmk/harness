import types
import pytest

import chainbreaker

@pytest.mark.skipif(
    not hasattr(chainbreaker, "Chainbreaker"),
    reason="Chainbreaker class not present in chainbreaker module"
)
def test_chainbreaker_attrs():
    # If the package structure is such that chainbreaker.Chainbreaker exists,
    # the rest of these tests will run, otherwise be skipped.
    class DummyDbBlob:
        Salt = b'\x00' * 8  # minimal, placeholder

    class DummyKC(chainbreaker.Chainbreaker):
        def __init__(self):
            self._unlock_password = "pw"
            self.dbblob = DummyDbBlob()
            self._generated = False
            self._unlock_key = None

        @property
        def unlock_password(self):
            return self._unlock_password

        @unlock_password.setter
        def unlock_password(self, value):
            self._unlock_password = value
            self._unlock_key = self._generate_master_key(value)
            self._generated = True

    kc = DummyKC()
    kc.unlock_password = "pw"
    assert kc._generated
    assert kc._unlock_key is not None

@pytest.mark.skipif(
    not hasattr(chainbreaker, "Chainbreaker"),
    reason="Chainbreaker class not present in chainbreaker module"
)
def test_class_has_logger():
    assert hasattr(chainbreaker.Chainbreaker, "logger")

@pytest.mark.skipif(
    not hasattr(chainbreaker, "Chainbreaker"),
    reason="Chainbreaker class not present in chainbreaker module"
)
def test_dump_generic_passwords_warns_if_keyerror(monkeypatch):
    class KCDummy(chainbreaker.Chainbreaker):
        def __init__(self):
            self.filepath = None
            self.unlock_password = None
            self.unlock_key = None
            self.unlock_file = None
        def _get_table_from_type(self, typ): raise KeyError()
        logger = types.SimpleNamespace(warning=lambda msg: setattr(self, "warned", msg))
    
    kc = KCDummy()
    kc.warned = None
    kc.dump_generic_passwords()
    assert kc.warned == '[!] Generic Password Table is not available'

@pytest.mark.skipif(
    not hasattr(chainbreaker, "Chainbreaker"),
    reason="Chainbreaker class not present in chainbreaker module"
)
def test_dump_internet_passwords_warn(monkeypatch):
    class KCDummy(chainbreaker.Chainbreaker):
        def __init__(self):
            self.filepath = None
            self.unlock_password = None
            self.unlock_key = None
            self.unlock_file = None
        def _get_table_from_type(self, typ): raise KeyError()
        logger = types.SimpleNamespace(warning=lambda msg: setattr(self, "warned", msg))
    
    kc = KCDummy()
    kc.warned = None
    kc.dump_internet_passwords()
    assert kc.warned == '[!] Internet Password Table is not available'
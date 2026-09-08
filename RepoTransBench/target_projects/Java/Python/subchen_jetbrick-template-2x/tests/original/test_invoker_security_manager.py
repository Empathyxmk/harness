import pytest

from tests.original.common import AbstractJetxTest

class TestSecurityManager(AbstractJetxTest):

    def initialize_engine(self):
        name_list = [
            "-java.io",
            "-java.lang.System",
            "-java.util.Date.<init>",
            "-java.lang.Integer.MAX_VALUE",
            "-java.lang.String.length",
            "-java.lang.CharSequence.length",
        ]
        security_manager = self.JetSecurityManagerImpl()
        security_manager.set_name_list(name_list)
        self.engine.set_security_manager(security_manager)

    def test_pkg_access(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${java.io.File::separator}")
        assert str(e.value).startswith("java.security.AccessControlException")

    def test_class_access(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${System::gc()}")
        assert str(e.value).startswith("java.security.AccessControlException")

    def test_constructor_access(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${new Date()}")
        assert str(e.value).startswith("java.security.AccessControlException")

    def test_method_access(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${'a'.length()}")
        assert str(e.value).startswith("java.security.AccessControlException")

    def test_field_access(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${Integer::MAX_VALUE}")
        assert str(e.value).startswith("java.security.AccessControlException")
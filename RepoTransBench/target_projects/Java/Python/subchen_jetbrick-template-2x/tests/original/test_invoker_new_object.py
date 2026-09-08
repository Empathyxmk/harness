import pytest

from tests.original.common import AbstractJetxTest

class TestInvokeNewObject(AbstractJetxTest):

    def initialize_engine(self):
        self.engine.get_global_resolver().import_class(self.Model.__module__ + ".*")
        self.engine.get_global_resolver().import_class(self.Model.__name__)

    def test_1(self):
        assert self.eval("${new Integer(1)}") == "1"
        assert self.eval("${new java.lang.Integer(1)}") == "1"
        assert self.eval("${new java.lang.Long(1)}") == "1"

    def test_2(self):
        assert self.eval("${new jetbrick.template.exec.invoker.InvokeNewObjectTest.Model()}") == "model"
        assert self.eval("${new jetbrick.template.exec.invoker.InvokeNewObjectTest.Model(1)}") == "model"
        assert self.eval("${new jetbrick.template.exec.invoker.InvokeNewObjectTest.Model(1L)}") == "model"

    def test_3(self):
        assert self.eval("${new Model()}") == "model"
        assert self.eval("${new InvokeNewObjectTest.Model()}") == "model"

    def test_class_not_found(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("${new Model12345()}")
        assert self.err(self.Errors.CLASS_NOT_FOUND) in str(e.value)

    def test_ctor_not_found(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${new Model(false)}")
        assert self.err(self.Errors.CONSTRUCTOR_NOT_FOUND) in str(e.value)

    class Model:
        def __str__(self):
            return "model"

        def __init__(self, n=None):
            pass
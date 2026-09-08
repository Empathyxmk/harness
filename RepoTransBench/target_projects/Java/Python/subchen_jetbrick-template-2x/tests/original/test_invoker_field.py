import pytest

from tests.original.common import AbstractJetxTest

class Model:
    VALUE = 10
    S_VAL = 20
    name = "model"
    good = True

    def isGood(self):
        return self.good

    def getName(self):
        return self.name

class TestInvokeField(AbstractJetxTest):

    def test(self):
        context = {"model": Model()}
        assert self.eval("${model.VALUE}", context) == "10"
        assert self.eval("${model.good}", context) == "true"
        assert self.eval("${model.name}", context) == "model"

    def test_not_found(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${''.xxx}")
        assert self.err(self.Errors.PROPERTY_NOT_FOUND) in str(e.value)

    def test_map(self):
        assert self.eval("${{name:'jetbrick'}.name}") == "jetbrick"
        assert self.eval("${{name:'jetbrick'}.xx}") == ""

    def test_array_length(self):
        context = {"model1": [0]*10, "model2": [None]*20}
        assert self.eval("${model1.length}", context) == "10"
        assert self.eval("${model2.length}", context) == "20"

    def test_class(self):
        assert self.eval("${'a'.class}") == "class java.lang.String"
        assert self.eval("${String::class}") == "class java.lang.String"

    def test_static(self):
        assert self.eval("${java.lang.Integer::MAX_VALUE}") == "2147483647"
        assert self.eval("${Integer::MAX_VALUE}") == "2147483647"

    def test_static_not_found(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${Integer::XXX}")
        assert self.err(self.Errors.STATIC_FIELD_NOT_FOUND) in str(e.value)
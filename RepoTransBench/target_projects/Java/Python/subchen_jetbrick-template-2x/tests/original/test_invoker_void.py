import pytest

from tests.original.common import AbstractJetxTest

class TestVoid(AbstractJetxTest):

    def test_value(self):
        assert self.eval("${Thread::yield()}") == ""
        assert self.eval("${new StringBuilder().trimToSize()}") == ""
        assert self.eval("$!{Thread::yield()}") == ""

    def test_argument_is_void(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${System::identityHashCode(Thread::yield())}")
        assert self.Errors.EXPRESSION_ARGUMENT_IS_VOID in str(e.value)

    def test_method_invoke(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${Thread::yield().toString()}")
        assert self.Errors.EXPRESSION_OBJECT_IS_VOID in str(e.value)

    def test_list_get1(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${Thread::yield()[0]}")
        assert self.Errors.EXPRESSION_OBJECT_IS_VOID in str(e.value)

    def test_list_get2(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${new StringBuilder().trimToSize()[0]}")
        assert self.Errors.EXPRESSION_OBJECT_IS_VOID in str(e.value)

    def test_list_get3(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${[1,2,3][Thread::yield()]}")
        assert self.Errors.EXPRESSION_INDEX_IS_VOID in str(e.value)
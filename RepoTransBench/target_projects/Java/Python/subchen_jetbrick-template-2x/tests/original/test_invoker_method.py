from tests.original.common import AbstractJetxTest

class TestInvokeMethod(AbstractJetxTest):

    class Model:
        def format(self, *args):
            if not args:
                return ""
            if len(args) == 1:
                return "{}".format(*args)
            if len(args) == 2:
                return "{}{}".format(*args)
            else:
                return "{}{}{}".format(*args)

    def test(self):
        assert self.eval("${'123456'.length()}") == "6"
        assert self.eval("${'123456'.charAt(1)}") == "2"

    def test_overload(self):
        assert self.eval("${'123456'.substring(3)}") == "456"
        assert self.eval("${'123456'.substring(3,5)}") == "45"

    def test_varargs(self):
        context = {"model": self.Model()}
        assert self.eval("${model.format()}", context) == ""
        assert self.eval("${model.format(1)}", context) == "1"
        assert self.eval("${model.format(1,2)}", context) == "12"
        assert self.eval("${model.format(1,2,3)}", context) == "123"

    def test_static(self):
        assert self.eval("${String::valueOf(12)}") == "12"
        assert self.eval("${java.lang.String::valueOf(12)}") == "12"

    def test_static_overload(self):
        assert self.eval("${String::valueOf(12)}") == "12"
        assert self.eval("${String::valueOf(12.99d)}") == "12.99"
        assert self.eval("${java.lang.String::valueOf(true)}") == "true"

    def test_static_varargs(self):
        assert self.eval("${String::format('aa')}") == "aa"
        assert self.eval("${String::format('%s', 'aa')}") == "aa"
        assert self.eval("${java.lang.String::format('%s%d', 'aa', 12)}") == "aa12"
from tests.original.common import AbstractJetxTest

class TestInvokeInterface(AbstractJetxTest):

    @classmethod
    def setup_class(cls):
        cls.ctx = {}

    def test(self):
        self.engine.set(self.DEFAULT_MAIN_FILE, "${x.intValue()}")
        template = self.engine.get_template(self.DEFAULT_MAIN_FILE)
        ctx = self.ctx
        ctx["x"] = 1
        assert self.eval(template, ctx) == "1"
        ctx["x"] = 1
        assert self.eval(template, ctx) == "1"
        ctx["x"] = 1
        assert self.eval(template, ctx) == "1"
        ctx["x"] = 1
        assert self.eval(template, ctx) == "1"
        ctx["x"] = 1
        assert self.eval(template, ctx) == "1"
        ctx["x"] = 1
        assert self.eval(template, ctx) == "1"
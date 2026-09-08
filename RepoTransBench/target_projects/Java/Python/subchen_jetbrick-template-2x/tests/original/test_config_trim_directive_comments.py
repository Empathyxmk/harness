from tests.original.common import AbstractJetxTest

class TestTrimDirectiveComments(AbstractJetxTest):

    def initialize_config(self):
        self.config.set_property(self.JetConfig.TRIM_DIRECTIVE_COMMENTS, "true")

    def test_basic(self):
        sb = "<!-- #for(int i:range(1,3)) -->\n${i}\n<!--#end-->"
        assert self.eval(sb) == "1\n2\n3\n"

    def test_multiline(self):
        sb = "<!-- \n    #for(int i:range(1,3))  \n -->  \n${i}\n<!--#end-->"
        assert self.eval(sb) == "1\n2\n3\n"

    def test_issue10(self):
        s = "<!-- #include('/sub.jetx') -->"
        self.engine.set(self.DEFAULT_MAIN_FILE, s)
        self.engine.set("/sub.jetx", "xxx")
        assert self.eval() == "xxx"
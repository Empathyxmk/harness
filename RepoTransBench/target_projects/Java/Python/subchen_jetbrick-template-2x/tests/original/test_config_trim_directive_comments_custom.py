from tests.original.common import AbstractJetxTest

class TestTrimDirectiveCommentsCustom(AbstractJetxTest):

    def initialize_config(self):
        self.config.set_property(self.JetConfig.TRIM_DIRECTIVE_COMMENTS, "true")
        self.config.set_property(self.JetConfig.TRIM_DIRECTIVE_COMMENTS_PREFIX, "<%--")
        self.config.set_property(self.JetConfig.TRIM_DIRECTIVE_COMMENTS_SUFFIX, "--%>")

    def test(self):
        assert self.eval("<%-- #stop --%>") == ""
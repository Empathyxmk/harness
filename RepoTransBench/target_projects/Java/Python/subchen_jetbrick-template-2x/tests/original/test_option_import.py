from tests.original.common import AbstractJetxTest

class TestOptionImport(AbstractJetxTest):

    def test_basic(self):
        assert self.eval("#options(import='java.text.DateFormat')${DateFormat::class}") == "class java.text.DateFormat"
        assert self.eval("#options(import='java.text.*')${DateFormat::class}") == "class java.text.DateFormat"

    def test_multi_pkgs(self):
        assert self.eval("#options(import='jetbrick.template.**')${ClasspathResourceLoader::class}") == "class jetbrick.template.loader.ClasspathResourceLoader"
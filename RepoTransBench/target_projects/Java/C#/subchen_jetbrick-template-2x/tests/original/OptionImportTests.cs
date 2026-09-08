using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class OptionImportTests : AbstractJetxTest
    {
        [Fact]
        public void TestBasic()
        {
            Assert.Equal("class java.text.DateFormat", Eval("#options(import='java.text.DateFormat')${DateFormat::class}"));
            Assert.Equal("class java.text.DateFormat", Eval("#options(import='java.text.*')${DateFormat::class}"));
        }

        [Fact]
        public void TestMultiPkgs()
        {
            Assert.Equal("class jetbrick.template.loader.ClasspathResourceLoader", Eval("#options(import='jetbrick.template.**')${ClasspathResourceLoader::class}"));
        }
    }
}
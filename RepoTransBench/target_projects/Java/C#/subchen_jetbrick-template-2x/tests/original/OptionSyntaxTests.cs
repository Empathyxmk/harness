using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class OptionSyntaxTests : AbstractJetxTest
    {
        [Fact]
        public void TestSyntax()
        {
            Eval("#options(import='java.io.*')");
            Eval("#options(strict=true, safecall=false, import='java.io.*', import='java.net.*')");
        }

        [Fact]
        public void TestInvalidName()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#options(unknown=true)"));
            Assert.Contains(Err(Errors.OPTION_NAME_INVALID), ex.Message);
        }

        [Fact]
        public void TestInvalidValue()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#options(strict=123)"));
            Assert.Contains(Err(Errors.OPTION_VALUE_INVALID), ex.Message);
        }
    }
}
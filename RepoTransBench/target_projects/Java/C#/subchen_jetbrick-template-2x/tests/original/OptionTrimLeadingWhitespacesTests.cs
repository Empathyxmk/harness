using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class OptionTrimLeadingWhitespacesTests : AbstractJetxTest
    {
        [Fact]
        public void Test()
        {
            Assert.Equal("", Eval("#options(trimLeadingWhitespaces=true)"));
            Assert.Equal("", Eval("#options(trimLeadingWhitespaces=true)\r\n"));
            Assert.Equal("abc\n", Eval("#options(trimLeadingWhitespaces=true)\r\nabc\n"));
        }
    }
}
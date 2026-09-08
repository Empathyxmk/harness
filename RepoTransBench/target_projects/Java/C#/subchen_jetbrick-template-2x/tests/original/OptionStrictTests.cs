using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class OptionStrictTests : AbstractJetxTest
    {
        [Fact]
        public void TestOk()
        {
            Eval("#options(strict=false)${a}");
        }

        [Fact]
        public void TestFail()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#options(strict=true)${a}"));
            Assert.Contains(Err(Errors.VARIABLE_UNDEFINED), ex.Message);
        }
    }
}
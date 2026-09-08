using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class OptionSafecallTests : AbstractJetxTest
    {
        [Fact]
        public void TestOk()
        {
            Eval("#options(safecall=true)${a.toString()}");
        }

        [Fact]
        public void TestFail()
        {
            var ex = Assert.Throws<InterpretException>(() => Eval("#options(safecall=false)${a.toString()}"));
            Assert.Contains(Errors.EXPRESSION_OBJECT_IS_NULL, ex.Message);
        }
    }
}
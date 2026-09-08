using System.Text;
using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class OptionLoadmacroTests : AbstractJetxTest
    {
        [Fact]
        public void TestInclude()
        {
            var s = new StringBuilder();
            s.Append("#options(loadmacro='/macros.jetx')");
            s.Append("#call size('abc')");
            s.Append("#call isOdd(123)");
            engine.Set(DEFAULT_MAIN_FILE, s.ToString());

            s = new StringBuilder();
            s.Append("#macro size(String s)");
            s.Append("${s.length()}");
            s.Append("#end");
            s.Append("#macro isOdd(int n)");
            s.Append("${n % 2 == 1}");
            s.Append("#end");
            engine.Set("/macros.jetx", s.ToString());

            Assert.Equal("3true", Eval());
        }
    }
}
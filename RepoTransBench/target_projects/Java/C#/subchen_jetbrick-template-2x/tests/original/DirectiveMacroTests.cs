using System.Text;
using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class DirectiveMacroTests : AbstractJetxTest
    {
        [Fact]
        public void TestDefinition()
        {
            var sb = new StringBuilder();
            sb.Append("#macro size(String s)");
            sb.Append("${s}, ${x}");
            sb.Append("#end");
            Eval(sb.ToString());
        }

        [Fact]
        public void TestRedefinition()
        {
            var sb = new StringBuilder();
            sb.Append("#macro size()#end");
            sb.Append("#macro size(int a)#end");
            var ex = Assert.Throws<SyntaxException>(() => Eval(sb.ToString()));
            Assert.Contains(Err(Errors.DIRECTIVE_MACRO_NAME_DUPLICATED), ex.Message);
        }

        [Fact]
        public void TestEmbed()
        {
            var sb = new StringBuilder();
            sb.Append("#macro size(String s)");
            sb.Append("size=${s.length()}");
            sb.Append("#end");
            sb.Append("#call size('abc')");
            Assert.Equal("size=3", Eval(sb.ToString()));
        }
    }
}
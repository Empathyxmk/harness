using System;
using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class DirectiveInvalidTests : AbstractJetxTest
    {
        [Fact]
        public void TestInvalidDefine()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#define"));
            Assert.Contains(Err(Errors.ARGUMENTS_MISSING), ex.Message);
        }

        [Fact]
        public void TestInvalidIf()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#if"));
            Assert.Contains(Err(Errors.ARGUMENTS_MISSING), ex.Message);
        }

        [Fact]
        public void TestInvalidMissingEnd()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#if(true)123"));
            Assert.Contains("mismatched input", ex.Message);
        }

        [Fact]
        public void TestInvalidBreak()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#break"));
            Assert.Contains("cannot be used outside of", ex.Message);
        }

        [Fact]
        public void TestInvalidContinue()
        {
            var ex = Assert.Throws<SyntaxException>(() => Eval("#continue"));
            Assert.Contains("cannot be used outside of", ex.Message);
        }
    }
}
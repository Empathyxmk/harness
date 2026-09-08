using System;
using System.Collections.Generic;
using System.Text;
using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class DirectiveIncludeTests : AbstractJetxTest
    {
        [Fact]
        public void TestInclude()
        {
            var s = new StringBuilder();
            s.Append("abc");
            s.Append("#include('/sub.jetx')");
            s.Append("123");
            engine.Set(DEFAULT_MAIN_FILE, s.ToString());

            s = new StringBuilder();
            s.Append("xxx");
            engine.Set("/sub.jetx", s.ToString());

            Assert.Equal("abcxxx123", Eval());
        }

        [Fact]
        public void TestIncludeArgs()
        {
            var s = new StringBuilder();
            s.Append("#set(c='c')");
            s.Append("${a}");
            s.Append("#include('/sub.jetx', {b:'b'})");
            s.Append("${c}");
            engine.Set(DEFAULT_MAIN_FILE, s.ToString());

            s = new StringBuilder();
            s.Append("<${a}-${b}-${c}>");
            engine.Set("/sub.jetx", s.ToString());

            var ctx = new Dictionary<string, object> { ["a"] = "a" };
            Assert.Equal("a<a-b-c>c", Eval(ctx));
        }

        [Fact]
        public void TestReturn()
        {
            var s = new StringBuilder();
            s.Append("${X}");
            s.Append("#include('/sub.jetx', 'X')");
            s.Append("${X}");
            engine.Set(DEFAULT_MAIN_FILE, s.ToString());

            s = new StringBuilder();
            s.Append("#return(12345)");
            engine.Set("/sub.jetx", s.ToString());

            Assert.Equal("12345", Eval());
        }
    }
}
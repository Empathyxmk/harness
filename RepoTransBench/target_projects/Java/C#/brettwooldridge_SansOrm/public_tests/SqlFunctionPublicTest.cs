using System;
using Xunit;

namespace SansOrm.Tests.Public
{
    public class SqlFunctionPublicTest
    {
        [Fact]
        public void TestApplyIntFunctionPublic()
        {
            Func<int, string> func = (v) => "Num" + (v + 3);
            Assert.Equal("Num8", func(5));
            Assert.Equal("Num12", func(9));
        }

        [Fact]
        public void TestApplyStringFunctionPublic()
        {
            Func<string, int> func = (s) => s.Length + 100;
            Assert.Equal(104, func("test"));
            Assert.Equal(110, func("abcdefghij"));
        }
    }
}
using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class TwigParserTests
    {
        [Fact]
        public void TestParseGetResult()
        {
            var parser = new TwigParser();
            var result = parser.Parse("something");
            Assert.NotNull(result);

            var result2 = parser.Parse("another");
            Assert.NotNull(result2);
        }
    }
}
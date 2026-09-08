using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigParserPublicTests
    {
        [Fact]
        public void TestParseWhitespacePublic()
        {
            var parser = new TwigParser();
            var result = parser.Parse("   ");
            Assert.NotNull(result);
            Assert.Empty(result.GetErrors());
        }

        [Fact]
        public void TestParseOutputTwigPublic()
        {
            var parser = new TwigParser();
            string input = "{{ 987 }}";
            var result = parser.Parse(input);
            Assert.NotNull(result);
            Assert.NotNull(result.GetParsedData());
        }
    }
}
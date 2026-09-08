using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigParserResultPublicTests
    {
        [Fact]
        public void TestBlankInputPublic()
        {
            var result = new TwigParserResult("   ");
            Assert.Empty(result.GetErrors());
            Assert.NotNull(result.GetParsedData());
        }

        [Fact]
        public void TestSimpleTwigInputPublic()
        {
            var result = new TwigParserResult("{% include 'header.twig' %}");
            Assert.NotNull(result.GetParsedData());
            Assert.NotNull(result.GetErrors());
        }
    }
}
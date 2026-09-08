using System;
using System.Collections.Generic;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class TwigParserResultTests
    {
        [Fact]
        public void TestConstructAndGetBlocks()
        {
            var res = new TwigParserResult("some");
            Assert.NotNull(res.GetErrors());
            // Should be modifiable (append)
            var errors = res.GetErrors();
            errors.Add("block");
            Assert.Contains("block", errors);
        }

        [Fact]
        public void TestBlockMethods()
        {
            var res = new TwigParserResult("desc");
            Assert.NotNull(res.GetParsedData());
        }
    }
}
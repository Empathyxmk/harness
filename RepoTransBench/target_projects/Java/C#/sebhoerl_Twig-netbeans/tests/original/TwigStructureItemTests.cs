using System;
using System.Collections.Generic;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class TwigStructureItemTests
    {
        [Fact]
        public void TestTwigStructureItemMethods()
        {
            var item = new TwigStructureItem("block", "METHOD", 1, 11);

            Assert.Equal("block", item.GetName());
            Assert.Equal("METHOD", item.GetKind());
            Assert.False(item.GetOffset() == 0 && item.GetEndOffset() == 0);
            Assert.Equal(1, item.GetOffset());
            Assert.Equal(11, item.GetEndOffset());
        }
    }
}
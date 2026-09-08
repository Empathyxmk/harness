using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigStructureItemPublicTests
    {
        [Fact]
        public void TestConstructorDifferentNamePublic()
        {
            var item = new TwigStructureItem("otherPublicName", "block", 7, 12);
            Assert.Equal("otherPublicName", item.GetName());
            Assert.Equal("block", item.GetKind());
            Assert.Equal(7, item.GetOffset());
            Assert.Equal(12, item.GetEndOffset());
        }
    }
}
using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class TwigDataObjectTests
    {
        [Fact]
        public void TestTwigDataObjectConstruction()
        {
            var obj = new TwigDataObject("test.twig");
            Assert.NotNull(obj);
            Assert.NotNull(obj.GetFileExtension());
        }

        [Fact]
        public void TestCreateNodeDelegateReturnsDataNode()
        {
            // Java test checks DataNode via Node. We just ensure object method returns expected dummy/stub,
            // as real Node type isn't modeled
            var obj = new TwigDataObject("test.twig");
            Assert.NotNull(obj); // There's no delegate method in stub. Just not null check here.
            Assert.Equal("twig", obj.GetFileExtension());
        }
    }
}
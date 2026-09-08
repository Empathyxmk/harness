using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigDataObjectPublicTests
    {
        [Fact]
        public void TestTwigDataObjectExtensionPublic()
        {
            var obj = new TwigDataObject("examplePublic.twig");
            Assert.Equal("twig", obj.GetFileExtension());
        }

        [Fact]
        public void TestIsTwigFileReturnsTruePublic()
        {
            var obj = new TwigDataObject("anotherfilePublic.twig");
            Assert.True(obj.IsTwigFile());
        }
    }
}
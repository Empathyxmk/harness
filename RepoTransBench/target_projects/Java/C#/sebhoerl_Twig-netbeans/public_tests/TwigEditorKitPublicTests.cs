using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigEditorKitPublicTests
    {
        [Fact]
        public void TestGetContentTypePublic()
        {
            var kit = new TwigEditorKit();
            Assert.Equal("text/x-twig-public", kit.GetContentType() + "-public");
        }

        [Fact]
        public void TestIsTwigEditorKitInstancePublic()
        {
            var kit = new TwigEditorKit();
            Assert.NotNull(kit);
            Assert.IsType<TwigEditorKit>(kit);
        }
    }
}
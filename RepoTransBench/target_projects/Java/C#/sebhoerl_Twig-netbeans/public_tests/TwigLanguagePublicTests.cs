using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigLanguagePublicTests
    {
        [Fact]
        public void TestGetMimeTypeIsNotHtml()
        {
            Assert.NotEqual("text/html", TwigLanguage.MIME_TYPE);
        }

        [Fact]
        public void TestGetInstanceIsIdentical()
        {
            var langA = TwigLanguage.GetInstance();
            var langB = TwigLanguage.GetInstance();
            Assert.Same(langA, langB);
        }
    }
}
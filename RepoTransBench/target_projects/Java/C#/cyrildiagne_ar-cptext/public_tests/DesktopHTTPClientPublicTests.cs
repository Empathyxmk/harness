using System;
using Xunit;
using Moq;
using ArCpText;

namespace ArCpText.PublicTests
{
    public class DesktopHTTPClientPublicTests
    {
        [Fact]
        public void TestGetAbsoluteUrlWithDifferentSuffix()
        {
            var url = DesktopHTTPClient.CallPrivateGetAbsoluteUrl("/public-data");
            Assert.True(url.EndsWith("/public-data") || url.Contains("/public-data"));
        }

        [Fact]
        public void TestSetDifferentPositionAndNoCrash()
        {
            DesktopHTTPClient.setPosition(5.5, -3.3);
        }

        [Fact]
        public void TestSetTextWithDifferentInputAndNoCrash()
        {
            DesktopHTTPClient.setText("This is a public test string!");
        }

        [Fact]
        public void TestPasteAndNoCrash_Public()
        {
            DesktopHTTPClient.paste();
        }

        [Fact]
        public void TestGetScreenshotReturnsNull_Public()
        {
            var cb = new Mock<DesktopHTTPClientCallback>().Object;
            var result = DesktopHTTPClient.getScreenshot(cb);
            Assert.Null(result);
        }
    }
}
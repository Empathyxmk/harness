using System;
using Xunit;
using Moq;
using ArCpText;

namespace ArCpText.Tests.Original
{
    public class DesktopHTTPClientTests
    {
        [Fact]
        public void TestGetAbsoluteUrl()
        {
            var url = DesktopHTTPClient.CallPrivateGetAbsoluteUrl("/test");
            Assert.Contains("/test", url);
        }

        [Fact]
        public void TestSetPositionAndNoCrash()
        {
            // Just call to test no exception
            DesktopHTTPClient.setPosition(1.0, 2.0);
        }

        [Fact]
        public void TestSetTextAndNoCrash()
        {
            DesktopHTTPClient.setText("Hello World");
        }

        [Fact]
        public void TestPasteAndNoCrash()
        {
            DesktopHTTPClient.paste();
        }

        [Fact]
        public void TestGetScreenshotReturnsNull()
        {
            var cb = new Mock<DesktopHTTPClientCallback>().Object;
            var result = DesktopHTTPClient.getScreenshot(cb);
            Assert.Null(result);
        }
    }
}
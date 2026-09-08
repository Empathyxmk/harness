using System;
using Xunit;
using Picasso;
using System.IO;

namespace PicassoTests.Public
{
    public class OkHttp3DownloaderLoadErrorPublicTest
    {
        [Fact]
        public void TestLoadThrowsOnInvalidProtocol()
        {
            var downloader = new OkHttp3Downloader();
            Assert.Throws<IOException>(() => downloader.Load("ftp://someurl", 0));
        }
    }
}
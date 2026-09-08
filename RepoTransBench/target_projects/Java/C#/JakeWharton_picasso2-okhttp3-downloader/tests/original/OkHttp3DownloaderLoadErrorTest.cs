using System;
using Xunit;

using Picasso;
using System.IO;

namespace PicassoTests.Original
{
    public class OkHttp3DownloaderLoadErrorTest
    {
        [Fact]
        public void TestLoadThrowsOnNullUrl()
        {
            var downloader = new OkHttp3Downloader();
            Assert.Throws<IOException>(() => downloader.Load(null, 0));
        }

        [Fact]
        public void TestLoadThrowsOnInvalidUrl()
        {
            var downloader = new OkHttp3Downloader();
            Assert.Throws<IOException>(() => downloader.Load("ftp://localhost/abc", 0));
        }

        [Fact]
        public void TestLoadSucceedsOnValidUrl()
        {
            var downloader = new OkHttp3Downloader();
            var result = downloader.Load("http://localhost/abc", 0);
            Assert.NotNull(result);
        }
    }
}
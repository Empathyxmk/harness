using System;
using Xunit;

using Picasso;

namespace PicassoTests.Original
{
    public class OkHttp3DownloaderTest
    {
        [Fact]
        public void TestShutdownDoesNotThrow()
        {
            var downloader = new OkHttp3Downloader();
            downloader.Shutdown();
        }

        [Fact]
        public void TestDummyConstructor()
        {
            var downloader = new OkHttp3Downloader("dummy");
        }
    }
}
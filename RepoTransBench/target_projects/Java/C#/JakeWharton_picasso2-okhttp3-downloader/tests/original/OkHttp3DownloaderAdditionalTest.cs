using System;
using System.IO;
using Xunit;

using Picasso;

namespace PicassoTests.Original
{
    public class OkHttp3DownloaderAdditionalTest
    {
        [Fact]
        public void TestLoadSucceedsWithDifferentNetworkPolicies()
        {
            var downloader = new OkHttp3Downloader();
            Assert.NotNull(downloader.Load("http://localhost/ok", 0));
            Assert.NotNull(downloader.Load("http://localhost/ok", -1));
            Assert.NotNull(downloader.Load("http://localhost/ok", 123));
        }

        [Fact]
        public void TestShutdownMultipleTimes()
        {
            var downloader = new OkHttp3Downloader();
            downloader.Shutdown();
            downloader.Shutdown(); // Should not throw
        }

        [Fact]
        public void TestLoadThrowsWhenUrlIsEmpty()
        {
            var downloader = new OkHttp3Downloader();
            Assert.Throws<IOException>(() => downloader.Load("", 0));
        }

        [Fact]
        public void TestAllConstructorsWithShutdown()
        {
            var d1 = new OkHttp3Downloader(new FileInfo("/tmp/cacheA"), 5L);
            var d2 = new OkHttp3Downloader(new FileInfo("/tmp/cacheB"));
            var d3 = new OkHttp3Downloader(123L);
            var d4 = new OkHttp3Downloader();
            var d5 = new OkHttp3Downloader("dummy2");
            d1.Shutdown();
            d2.Shutdown();
            d3.Shutdown();
            d4.Shutdown();
            d5.Shutdown();
        }
    }
}
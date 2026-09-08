using System;
using System.IO;
using Xunit;

using Picasso;

namespace PicassoTests.Public
{
    public class OkHttp3DownloaderAdditionalPublicTest
    {
        [Fact]
        public void TestLoadSucceedsWithOtherNetworkPolicies()
        {
            var downloader = new OkHttp3Downloader();
            Assert.NotNull(downloader.Load("http://127.0.0.1/success", 1));
            Assert.NotNull(downloader.Load("http://127.0.0.1/success", 42));
            Assert.NotNull(downloader.Load("http://127.0.0.1/success", -100));
        }

        [Fact]
        public void TestShutdownManyTimes()
        {
            var downloader = new OkHttp3Downloader();
            downloader.Shutdown();
            downloader.Shutdown();
            downloader.Shutdown(); // Should not throw
        }

        [Fact]
        public void TestLoadThrowsWhenUrlIsNullString()
        {
            var downloader = new OkHttp3Downloader();
            Assert.Throws<IOException>(() => downloader.Load(null, 0));
        }

        [Fact]
        public void TestAllConstructorsWithShutdownPublic()
        {
            var d1 = new OkHttp3Downloader(new FileInfo("/tmp/pub_cacheA"), 15L);
            var d2 = new OkHttp3Downloader(new FileInfo("/tmp/pub_cacheB"));
            var d3 = new OkHttp3Downloader(321L);
            var d4 = new OkHttp3Downloader();
            var d5 = new OkHttp3Downloader("publicDummy");
            d1.Shutdown();
            d2.Shutdown();
            d3.Shutdown();
            d4.Shutdown();
            d5.Shutdown();
        }
    }
}
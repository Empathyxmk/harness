using System;
using Xunit;

using Picasso;

namespace PicassoTests.Public
{
    public class OkHttp3DownloaderPublicTest
    {
        [Fact]
        public void TestShutdownIsSafeRepeatedly()
        {
            var downloader = new OkHttp3Downloader();
            downloader.Shutdown();
            downloader.Shutdown();
        }

        [Fact]
        public void TestAnotherDummyConstructor()
        {
            var downloader = new OkHttp3Downloader("publicValue");
        }
    }
}
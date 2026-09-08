using System;
using System.IO;
using Xunit;

using Picasso;

namespace PicassoTests.Public
{
    public class OkHttp3DownloaderCtorPublicTest
    {
        [Fact]
        public void TestPublicCtorWithCacheDir()
        {
            var file = new FileInfo("/tmp/public_ctor_cache");
            var downloader = new OkHttp3Downloader(file);
        }

        [Fact]
        public void TestPublicCtorWithCacheDirAndMaxSize()
        {
            var file = new FileInfo("/tmp/public_ctor_cache2");
            var downloader = new OkHttp3Downloader(file, 2048L);
        }

        [Fact]
        public void TestPublicCtorWithMaxSize()
        {
            var downloader = new OkHttp3Downloader(8192L);
        }
    }
}
using System;
using System.IO;
using Xunit;

using Picasso;

namespace PicassoTests.Public
{
    public class OkHttp3DownloaderDiskCachePublicTest
    {
        [Fact]
        public void TestCtorWithAnotherCacheDir()
        {
            var file = new FileInfo("/tmp/pub_cache_c");
            var downloader = new OkHttp3Downloader(file);
        }

        [Fact]
        public void TestCtorWithAnotherCacheDirAndMaxSize()
        {
            var file = new FileInfo("/tmp/pub_cache_d");
            var downloader = new OkHttp3Downloader(file, 5555L);
        }

        [Fact]
        public void TestCtorWithAnotherMaxSize()
        {
            var downloader = new OkHttp3Downloader(9876L);
        }
    }
}
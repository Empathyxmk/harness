using System;
using System.IO;
using Xunit;

using Picasso;

namespace PicassoTests.Original
{
    public class OkHttp3DownloaderDiskCacheTest
    {
        [Fact]
        public void TestCtorWithCacheDir()
        {
            var file = new FileInfo("/tmp/cache");
            var downloader = new OkHttp3Downloader(file);
            // Just check for exceptions
        }

        [Fact]
        public void TestCtorWithCacheDirAndMaxSize()
        {
            var file = new FileInfo("/tmp/cache");
            var downloader = new OkHttp3Downloader(file, 1024L);
            // Just check for exceptions
        }

        [Fact]
        public void TestCtorWithMaxSize()
        {
            var downloader = new OkHttp3Downloader(4096L);
            // Just check for exceptions
        }
    }
}
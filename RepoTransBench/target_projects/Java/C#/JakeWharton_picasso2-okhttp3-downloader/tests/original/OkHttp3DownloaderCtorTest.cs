using System;
using Xunit;

using Picasso;

namespace PicassoTests.Original
{
    public class OkHttp3DownloaderCtorTest
    {
        [Fact]
        public void TestNoArgCtor()
        {
            var downloader = new OkHttp3Downloader();
        }
    }
}
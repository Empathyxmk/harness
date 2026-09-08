using System.IO;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.PublicTests
{
    /// <summary>
    /// Public tests for ChannelReader: test methods with different data focus on
    /// null and missing files (since core logic requires valid APKs, which can't be unit tested simply).
    /// </summary>
    public class ChannelReaderPublicTest
    {
        [Fact]
        public void TestGetChannelByFile_Public()
        {
            var file = new FileInfo("nonexistent-public.apk");
            Assert.Null(ChannelReader.GetChannel(file));
        }

        [Fact]
        public void TestGetChannelInfoByFile_Public()
        {
            var file = new FileInfo("not-there-and-public.apk");
            Assert.Null(ChannelReader.GetChannelInfo(file));
        }
    }
}
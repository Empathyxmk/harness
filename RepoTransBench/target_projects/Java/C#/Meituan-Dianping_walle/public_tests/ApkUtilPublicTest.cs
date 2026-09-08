using System.Reflection;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.PublicTests
{
    public class ApkUtilPublicTest
    {
        [Fact]
        public void TestApkSigBlockMagicConstants_Public()
        {
            // Use reflection to get the constants for extra validation
            var hi = typeof(ApkUtil).GetField("APK_SIG_BLOCK_MAGIC_HI", BindingFlags.Static | BindingFlags.Public);
            var lo = typeof(ApkUtil).GetField("APK_SIG_BLOCK_MAGIC_LO", BindingFlags.Static | BindingFlags.Public);

            Assert.Equal(0x3234206b636f6c42L, (long)hi.GetValue(null));
            Assert.Equal(0x20676953204b5041L, (long)lo.GetValue(null));
        }

        [Fact]
        public void TestDefaultCharset_Public()
        {
            Assert.Equal("UTF-8", ApkUtil.DEFAULT_CHARSET);
        }

        [Fact]
        public void TestChannelBlockId_Public()
        {
            Assert.Equal(0x71777777, ApkUtil.APK_CHANNEL_BLOCK_ID);
        }
    }
}
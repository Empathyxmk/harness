using System.Collections.Generic;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.PublicTests
{
    public class ChannelInfoPublicTest
    {
        [Fact]
        public void TestGettersAndToString_Public()
        {
            var info = new Dictionary<string, string> { { "testKey", "testVal" } };
            var channelInfo = new ChannelInfo("pub-channel", info);

            Assert.Equal("pub-channel", channelInfo.Channel);
            Assert.Equal("testVal", channelInfo.ExtraInfo["testKey"]);
            Assert.Contains("pub-channel", channelInfo.ToString());
            Assert.Contains("testKey", channelInfo.ToString());
            Assert.Contains("testVal", channelInfo.ToString());
        }

        [Fact]
        public void TestNullExtraInfo_Public()
        {
            var channelInfo = new ChannelInfo("pub-label", null);
            Assert.Equal("pub-label", channelInfo.Channel);
            Assert.Null(channelInfo.ExtraInfo);
            Assert.Contains("pub-label", channelInfo.ToString());
            Assert.Contains("null", channelInfo.ToString());
        }
    }
}
using System.Collections.Generic;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.Tests
{
    public class ChannelInfoTest
    {
        [Fact]
        public void TestConstructorAndGetters_Basic()
        {
            var extra = new Dictionary<string, string> { { "k1", "v1" } };
            var info = new ChannelInfo("channelA", extra);
            Assert.Equal("channelA", info.Channel);
            Assert.Equal(extra, info.ExtraInfo);
        }

        [Fact]
        public void TestConstructorAndGetters_NullExtra()
        {
            var info = new ChannelInfo("abc", null);
            Assert.Equal("abc", info.Channel);
            Assert.Null(info.ExtraInfo);
        }

        [Fact]
        public void TestConstructorAndGetters_NullChannel()
        {
            var extra = new Dictionary<string, string>();
            var info = new ChannelInfo(null, extra);
            Assert.Null(info.Channel);
            Assert.Equal(extra, info.ExtraInfo);
        }
    }
}
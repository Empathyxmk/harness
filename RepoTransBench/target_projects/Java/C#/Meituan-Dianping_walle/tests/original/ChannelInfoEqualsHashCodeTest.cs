using System.Collections.Generic;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.Tests
{
    public class ChannelInfoEqualsHashCodeTest
    {
        [Fact]
        public void TestEqualsAndHashCode()
        {
            var extraA = new Dictionary<string, string>
            {
                { "foo", "bar" }
            };
            var a = new ChannelInfo("ch", extraA);
            var b = new ChannelInfo("ch", extraA);
            Assert.Equal(a, b);
            Assert.Equal(a.GetHashCode(), b.GetHashCode());

            // different channel
            var c = new ChannelInfo("c2", extraA);
            Assert.NotEqual(a, c);

            // different extraInfo
            var d = new ChannelInfo("ch", null);
            Assert.NotEqual(a, d);

            // null channel
            var e = new ChannelInfo(null, extraA);
            var f = new ChannelInfo(null, extraA);
            Assert.Equal(e, f);
            Assert.Equal(e.GetHashCode(), f.GetHashCode());
        }
    }
}
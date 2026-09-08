using System.Collections.Generic;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.PublicTests
{
    public class ChannelInfoEqualsHashCodePublicTest
    {
        [Fact]
        public void TestEqualsAndHashCode_Public()
        {
            var extraA = new Dictionary<string, string> { { "baz", "qux" } };
            var a = new ChannelInfo("public", extraA);
            var b = new ChannelInfo("public", extraA);
            Assert.Equal(a, b);
            Assert.Equal(a.GetHashCode(), b.GetHashCode());

            // different channel
            var c = new ChannelInfo("diff", extraA);
            Assert.NotEqual(a, c);

            // different extraInfo
            var d = new ChannelInfo("public", null);
            Assert.NotEqual(a, d);

            // null channel
            var e = new ChannelInfo(null, extraA);
            var f = new ChannelInfo(null, extraA);
            Assert.Equal(e, f);
            Assert.Equal(e.GetHashCode(), f.GetHashCode());
        }
    }
}
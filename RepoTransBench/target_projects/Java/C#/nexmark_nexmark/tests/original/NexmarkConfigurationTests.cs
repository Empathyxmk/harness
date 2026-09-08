using System;
using Xunit;
using NexmarkFlink;
using NexmarkFlink.utils;

namespace OriginalTests
{
    public class NexmarkConfigurationTests
    {
        [Fact]
        public void TestDefaultValues()
        {
            var config = new NexmarkConfiguration();
            Assert.Equal(0, config.NumEvents);
            Assert.Equal(1, config.NumEventGenerators);
            Assert.Equal(NexmarkUtils.RateShape.SQUARE, config.RateShape);
            Assert.Equal(10000, config.FirstEventRate);
            Assert.Equal(10000, config.NextEventRate);
            Assert.Equal(NexmarkUtils.RateUnit.PER_SECOND, config.RateUnit);
            Assert.Equal(600, config.RatePeriodSec);
            Assert.Equal(0, config.PreloadSeconds);
            Assert.Equal(240, config.StreamTimeout);
            Assert.False(config.IsRateLimited);
            Assert.False(config.UseWallclockEventTime);
            Assert.Equal(1, config.PersonProportion);
            Assert.Equal(3, config.AuctionProportion);
            Assert.Equal(46, config.BidProportion);
            Assert.Equal(200, config.AvgPersonByteSize);
            Assert.Equal(500, config.AvgAuctionByteSize);
            Assert.Equal(100, config.AvgBidByteSize);
            Assert.Equal(2, config.HotAuctionRatio);
            Assert.Equal(4, config.HotSellersRatio);
            Assert.Equal(4, config.HotBiddersRatio);
            Assert.Equal(10, config.WindowSizeSec);
            Assert.Equal(5, config.WindowPeriodSec);
            Assert.Equal(0, config.WatermarkHoldbackSec);
            Assert.Equal(100, config.NumInFlightAuctions);
            Assert.Equal(1000, config.NumActivePeople);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var c1 = new NexmarkConfiguration();
            var c2 = new NexmarkConfiguration();
            Assert.Equal(c1, c2);
            Assert.Equal(c1.GetHashCode(), c2.GetHashCode());
            c2.NumEvents = 100;
            Assert.NotEqual(c1, c2);
        }
    }
}
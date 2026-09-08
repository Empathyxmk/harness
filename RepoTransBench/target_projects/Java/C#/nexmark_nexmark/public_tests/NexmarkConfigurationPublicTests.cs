using System;
using Xunit;
using NexmarkFlink;
using NexmarkFlink.utils;

namespace PublicTests
{
    public class NexmarkConfigurationPublicTests
    {
        [Fact]
        public void TestDefaultValuesAreNotAllCustom()
        {
            var config = new NexmarkConfiguration();
            Assert.NotEqual(1, config.NumEvents);
            Assert.Equal(NexmarkUtils.RateShape.SQUARE, config.RateShape);
            Assert.NotEqual(20000, config.FirstEventRate);
            Assert.Equal(NexmarkUtils.RateUnit.PER_SECOND, config.RateUnit);
            Assert.NotEqual(1200, config.RatePeriodSec);
            Assert.True(config.PersonProportion < config.BidProportion);
            Assert.NotEqual(300, config.AvgPersonByteSize);
            Assert.NotEqual(999, config.NumInFlightAuctions);
            Assert.True(config.NumActivePeople > 0);
        }

        [Fact]
        public void TestEqualsAndHashCodeDiffObject()
        {
            var c1 = new NexmarkConfiguration();
            var c2 = new NexmarkConfiguration();
            c1.FirstEventRate = 12345;
            Assert.NotEqual(c1, c2);
            c2.FirstEventRate = 12345;
            Assert.Equal(c1, c2);
            Assert.Equal(c1.GetHashCode(), c2.GetHashCode());
        }
    }
}
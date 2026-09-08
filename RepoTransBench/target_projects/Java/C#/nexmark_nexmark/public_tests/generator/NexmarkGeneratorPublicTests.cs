using System;
using Xunit;
using NexmarkFlink.generator;

namespace PublicTests.generator
{
    public class NexmarkGeneratorPublicTests
    {
        [Fact]
        public void TestInitialEventGeneration()
        {
            var generator = new NexmarkGenerator(250L, 1, 500L, 3, 99);
            Assert.NotNull(generator.NextEvent());
            Assert.Equal(1, generator.GetMaxPersonId());
        }

        [Fact]
        public void TestBidSequenceGenerated()
        {
            var generator = new NexmarkGenerator(20L, 2, 100L, 2, 66);
            for (int i = 0; i < 5; i++)
            {
                Assert.NotNull(generator.NextEvent());
            }
            Assert.True(generator.GetMaxAuctionId() > 0);
        }
    }
}
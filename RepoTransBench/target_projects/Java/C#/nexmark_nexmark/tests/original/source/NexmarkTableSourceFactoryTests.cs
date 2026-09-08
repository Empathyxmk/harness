using System;
using System.Collections.Generic;
using Xunit;
using NexmarkFlink.source;
using NexmarkFlink;
using NexmarkFlink.generator;
using NexmarkFlink.utils;

namespace OriginalTests.source
{
    public class NexmarkTableSourceFactoryTests
    {
        [Fact]
        public void TestCommonProperties()
        {
            var properties = GetAllOptions();

            var actualSource = CreateTableSource(properties);
            var config = new GeneratorConfig(
                new NexmarkConfiguration(),
                DateTimeOffset.Now.ToUnixTimeMilliseconds(),
                1,
                0,
                1
            );
            var expectedSource = new NexmarkTableSource(config);
            Assert.Equal(expectedSource, actualSource);
        }

        [Fact]
        public void TestCustomProperties()
        {
            var properties = GetAllOptions();
            properties["rate.shape"] = "SQUARE";
            properties["rate.period"] = "11 min";
            properties["rate.limited"] = "true";
            properties["first-event.rate"] = "99";
            properties["next-event.rate"] = "199";
            properties["person.avg-size"] = "1kb";
            properties["auction.avg-size"] = "5kb";
            properties["bid.avg-size"] = "8kb";
            properties["person.proportion"] = "30";
            properties["auction.proportion"] = "15";
            properties["bid.proportion"] = "5";
            properties["bid.hot-ratio.auctions"] = "3";
            properties["bid.hot-ratio.bidders"] = "5";
            properties["auction.hot-ratio.sellers"] = "8";
            properties["events.num"] = "100";

            var actualSource = CreateTableSource(properties);
            var nexmarkConf = new NexmarkConfiguration
            {
                RateShape = NexmarkUtils.RateShape.SQUARE,
                RatePeriodSec = 11 * 60,
                IsRateLimited = true,
                FirstEventRate = 99,
                NextEventRate = 199,
                AvgPersonByteSize = 1024,
                AvgAuctionByteSize = 5 * 1024,
                AvgBidByteSize = 8 * 1024,
                PersonProportion = 30,
                AuctionProportion = 15,
                BidProportion = 5,
                HotAuctionRatio = 3,
                HotBiddersRatio = 5,
                HotSellersRatio = 8,
                NumEvents = 100
            };

            var config = new GeneratorConfig(
                nexmarkConf,
                DateTimeOffset.Now.ToUnixTimeMilliseconds(),
                1,
                nexmarkConf.NumEvents,
                1
            );
            var expectedSource = new NexmarkTableSource(config);
            Assert.Equal(expectedSource, actualSource);
        }

        private Dictionary<string, string> GetAllOptions()
        {
            return new Dictionary<string, string> { { "connector", "nexmark" } };
        }

        private NexmarkTableSource CreateTableSource(Dictionary<string, string> options)
        {
            // This function would mimic the factory util in Java; here stub for logic equivalence.
            return NexmarkTableSourceFactory.CreateDynamicTableSource(options);
        }
    }
}
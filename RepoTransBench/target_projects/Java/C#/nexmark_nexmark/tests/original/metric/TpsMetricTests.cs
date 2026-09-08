using System;
using Xunit;
using NexmarkFlink.metric.tps;

namespace OriginalTests.metric
{
    public class TpsMetricTests
    {
        [Fact]
        public void TestParseJson()
        {
            string json = @"
            [
                {
                  ""id"": ""Source__TableSourceScan(table=[[default_catalog__default_database__nexmark]]__fi.numRecordsOutPerSecond"",
                  ""min"": 5003.2,
                  ""max"": 5003.2,
                  ""avg"": 5003.2,
                  ""sum"": 10006.3
                }
            ]";

            var tps = TpsMetric.FromJson(json);
            var expected = new TpsMetric(
                "Source__TableSourceScan(table=[[default_catalog__default_database__nexmark]]__fi.numRecordsOutPerSecond",
                5003.2,
                5003.2,
                5003.2,
                10006.3);
            Assert.Equal(expected, tps);
        }
    }
}
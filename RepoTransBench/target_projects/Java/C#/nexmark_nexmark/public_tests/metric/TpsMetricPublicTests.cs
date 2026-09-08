using System;
using Xunit;
using NexmarkFlink.metric.tps;

namespace PublicTests.metric
{
    public class TpsMetricPublicTests
    {
        [Fact]
        public void TestTpsMetricSettersGetters()
        {
            var metric = new TpsMetric();
            metric.StartTime = 22222L;
            metric.EndTime = 33333L;
            metric.Tps = 12345.6;
            metric.Num = 77L;

            Assert.Equal(22222L, metric.StartTime);
            Assert.Equal(33333L, metric.EndTime);
            Assert.Equal(12345.6, metric.Tps);
            Assert.Equal(77L, metric.Num);
        }
    }
}
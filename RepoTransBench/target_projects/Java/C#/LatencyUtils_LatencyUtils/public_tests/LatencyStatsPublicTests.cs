using System;
using Xunit;

namespace LatencyUtils.Tests.Public
{
    public class LatencyStatsPublicTests
    {
        [Fact]
        public void TestRecordAndEstimate()
        {
            var stats = new LatencyStats();
            for (int i = 0; i < 50; i++)
            {
                stats.RecordLatency(2000 + i * 2); // Use a different base and increment
            }
            long est = stats.GetIntervalHistogram().GetMaxValue();
            Assert.True(est >= 2000);
        }
    }
}
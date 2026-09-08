using System;
using Xunit;
using NexmarkFlink.metric.cpu;
using NexmarkFlink.utils;
using System.Collections.Generic;

namespace OriginalTests.metric
{
    public class CpuMetricTests
    {
        [Fact]
        public void TestCpuMetric()
        {
            var cpuMetrics = new List<CpuMetric>
            {
                new CpuMetric("10.0.0.12", 37927, 1.01),
                new CpuMetric("10.1.0.33", 54389, 2.3),
                new CpuMetric("10.2.0.44", 4401, 0.4)
            };
            var result = NexmarkUtils.MapperWriteValue(cpuMetrics);

            var expected = CpuMetric.FromJsonArray(result);
            Assert.Equal(expected, cpuMetrics);
        }
    }
}
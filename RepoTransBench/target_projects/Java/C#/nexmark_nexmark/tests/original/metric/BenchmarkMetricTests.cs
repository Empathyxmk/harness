using System;
using Xunit;
using NexmarkFlink.metric;

namespace OriginalTests.metric
{
    public class BenchmarkMetricTests
    {
        [Fact]
        public void TestFormatLongValue()
        {
            Assert.Equal("1.64 M", BenchmarkMetric.FormatLongValue(1636000));
            Assert.Equal("1.6 M", BenchmarkMetric.FormatLongValue(1600000));
            Assert.Equal("232", BenchmarkMetric.FormatLongValue(232));
            Assert.Equal("23.21 K", BenchmarkMetric.FormatLongValue(23213));
        }
    }
}
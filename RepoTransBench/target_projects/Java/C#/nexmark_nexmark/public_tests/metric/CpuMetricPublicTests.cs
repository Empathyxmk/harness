using System;
using Xunit;
using NexmarkFlink.metric.cpu;

namespace PublicTests.metric
{
    public class CpuMetricPublicTests
    {
        [Fact]
        public void TestCpuMetricDifferentValues()
        {
            var metric = new CpuMetric(234.56, 1900L, 14.7f, 100.2, "nodeX");
            Assert.Equal(234.56, metric.ProcessCpuTimeSeconds);
            Assert.Equal(1900L, metric.ProcessTotalCpuMilliseconds);
            Assert.Equal(14.7f, metric.ProcessCpuLoad);
            Assert.Equal(100.2, metric.SystemCpuLoad);
            Assert.Equal("nodeX", metric.HostName);
        }

        [Fact]
        public void TestToStringNotEmpty()
        {
            var metric = new CpuMetric(0.99, 99L, 2.2f, 88.1, "hostY");
            var s = metric.ToString();
            Assert.Contains("hostY", s);
            Assert.True(s.Length > 0);
        }
    }
}
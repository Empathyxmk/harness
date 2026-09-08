using System;
using Xunit;
using NexmarkFlink.metric;
using System.Globalization;

namespace PublicTests.metric
{
    public class BenchmarkMetricPublicTests
    {
        [Fact]
        public void TestFormatDoubleValuePublic()
        {
            double value = 98765.4321;
            var formatted = BenchmarkMetric.FormatDoubleValue(value);
            var expected = value.ToString("N", CultureInfo.InvariantCulture);
            Assert.Equal(expected, formatted);
        }

        [Fact]
        public void TestFormatLongValuePerSecondPublic()
        {
            long value = 543210;
            double seconds = 36.0;
            var formatted = BenchmarkMetric.FormatLongValuePerSecond(value, seconds);
            Assert.Contains("/s", formatted);
            Assert.DoesNotContain("N/A", formatted);
        }
    }
}
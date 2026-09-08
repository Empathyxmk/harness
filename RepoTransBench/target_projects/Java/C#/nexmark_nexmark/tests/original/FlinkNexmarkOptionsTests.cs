using System;
using Xunit;
using NexmarkFlink;

namespace OriginalTests
{
    public class FlinkNexmarkOptionsTests
    {
        [Fact]
        public void TestMetricMonitorDelayDefaults()
        {
            var option = FlinkNexmarkOptions.METRIC_MONITOR_DELAY;
            Assert.Equal("nexmark.metric.monitor.delay", option.Key);
            Assert.Equal(TimeSpan.FromSeconds(10), option.DefaultValue);
        }

        [Fact]
        public void TestMetricMonitorDurationDefaults()
        {
            var option = FlinkNexmarkOptions.METRIC_MONITOR_DURATION;
            Assert.Equal("nexmark.metric.monitor.duration", option.Key);
            Assert.Equal(TimeSpan.FromTicks(long.MaxValue), option.DefaultValue); // No nanoseconds in C#
        }

        [Fact]
        public void TestMetricMonitorIntervalDefaults()
        {
            var option = FlinkNexmarkOptions.METRIC_MONITOR_INTERVAL;
            Assert.Equal("nexmark.metric.monitor.interval", option.Key);
            Assert.Equal(TimeSpan.FromSeconds(5), option.DefaultValue);
        }

        [Fact]
        public void TestMetricReporterHostDefaults()
        {
            var option = FlinkNexmarkOptions.METRIC_REPORTER_HOST;
            Assert.Equal("nexmark.metric.reporter.host", option.Key);
            Assert.Equal("localhost", option.DefaultValue);
        }

        [Fact]
        public void TestMetricReporterPortDefaults()
        {
            var option = FlinkNexmarkOptions.METRIC_REPORTER_PORT;
            Assert.Equal("nexmark.metric.reporter.port", option.Key);
            Assert.Equal(9098, option.DefaultValue);
        }

        [Fact]
        public void TestFlinkRestAddressDefaults()
        {
            var option = FlinkNexmarkOptions.FLINK_REST_ADDRESS;
            Assert.Equal("flink.rest.address", option.Key);
            Assert.Equal("localhost", option.DefaultValue);
        }

        [Fact]
        public void TestFlinkRestPortDefaults()
        {
            var option = FlinkNexmarkOptions.FLINK_REST_PORT;
            Assert.Equal("flink.rest.port", option.Key);
            Assert.Equal(8081, option.DefaultValue);
        }
    }
}
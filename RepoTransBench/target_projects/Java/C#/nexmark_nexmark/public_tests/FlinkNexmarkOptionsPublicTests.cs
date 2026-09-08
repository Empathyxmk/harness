using System;
using Xunit;
using NexmarkFlink;

namespace PublicTests
{
    public class FlinkNexmarkOptionsPublicTests
    {
        [Fact]
        public void TestMetricMonitorDelayKeyAndType()
        {
            var option = FlinkNexmarkOptions.METRIC_MONITOR_DELAY;
            Assert.Equal("nexmark.metric.monitor.delay", option.Key);
            Assert.NotEqual(TimeSpan.FromSeconds(30), option.DefaultValue);
        }

        [Fact]
        public void TestMetricMonitorDurationKeyAndType()
        {
            var option = FlinkNexmarkOptions.METRIC_MONITOR_DURATION;
            Assert.Equal("nexmark.metric.monitor.duration", option.Key);
            Assert.True(option.DefaultValue > TimeSpan.FromDays(365));
        }

        [Fact]
        public void TestMetricMonitorIntervalKeyAndType()
        {
            var option = FlinkNexmarkOptions.METRIC_MONITOR_INTERVAL;
            Assert.Equal("nexmark.metric.monitor.interval", option.Key);
            Assert.NotEqual(TimeSpan.FromSeconds(2), option.DefaultValue);
        }

        [Fact]
        public void TestMetricReporterHostKeyAndType()
        {
            var option = FlinkNexmarkOptions.METRIC_REPORTER_HOST;
            Assert.Equal("nexmark.metric.reporter.host", option.Key);
            Assert.NotEqual("nexmark", option.DefaultValue);
        }

        [Fact]
        public void TestMetricReporterPortKeyAndType()
        {
            var option = FlinkNexmarkOptions.METRIC_REPORTER_PORT;
            Assert.Equal("nexmark.metric.reporter.port", option.Key);
            Assert.NotEqual(9000, option.DefaultValue);
        }

        [Fact]
        public void TestFlinkRestAddressKeyAndType()
        {
            var option = FlinkNexmarkOptions.FLINK_REST_ADDRESS;
            Assert.Equal("flink.rest.address", option.Key);
            Assert.NotEqual("127.0.0.1", option.DefaultValue);
        }

        [Fact]
        public void TestFlinkRestPortKeyAndType()
        {
            var option = FlinkNexmarkOptions.FLINK_REST_PORT;
            Assert.Equal("flink.rest.port", option.Key);
            Assert.NotEqual(8000, option.DefaultValue);
        }
    }
}
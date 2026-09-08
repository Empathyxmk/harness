using System;
using Xunit;
using NexmarkFlink.metric.cpu;

namespace PublicTests.metric
{
    public class CpuMetricSenderPublicTests
    {
        [Fact]
        public void TestMetricSenderHostAndPort()
        {
            var sender = new CpuMetricSender("testhost", 10000);
            Assert.Equal("testhost", sender.Host);
            Assert.Equal(10000, sender.Port);
        }

        [Fact]
        public void TestMetricSenderNegativePort()
        {
            var sender = new CpuMetricSender("anotherhost", -1);
            Assert.Equal(-1, sender.Port);
        }
    }
}
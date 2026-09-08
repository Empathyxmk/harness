using System;
using Xunit;
using NexmarkFlink.metric;

namespace PublicTests.metric
{
    public class FlinkRestClientPublicTests
    {
        [Fact]
        public void TestAddressWithPort()
        {
            var client = new FlinkRestClient("192.168.0.100", 9000);
            Assert.Equal("192.168.0.100", client.RestAddress);
            Assert.Equal(9000, client.RestPort);
        }

        [Fact]
        public void TestRestAddressNotDefault()
        {
            var client = new FlinkRestClient("example.com", 12345);
            Assert.NotEqual("localhost", client.RestAddress);
            Assert.Equal(12345, client.RestPort);
        }
    }
}
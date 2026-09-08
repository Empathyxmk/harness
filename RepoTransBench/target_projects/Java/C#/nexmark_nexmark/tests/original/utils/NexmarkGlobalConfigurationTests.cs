using System;
using Xunit;
using NexmarkFlink.utils;
using Microsoft.Extensions.Configuration;

namespace OriginalTests.utils
{
    public class NexmarkGlobalConfigurationTests
    {
        [Fact]
        public void TestLoadConfiguration()
        {
            var confDir = "src/main/resources/conf";
            var conf = NexmarkGlobalConfiguration.LoadConfiguration(confDir);
            Assert.Equal(8081, conf["flink.rest.port"]);
            Assert.Equal("localhost", conf["flink.rest.address"]);
        }
    }
}
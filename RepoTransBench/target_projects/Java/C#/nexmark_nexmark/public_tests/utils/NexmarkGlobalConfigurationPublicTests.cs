using System;
using Xunit;
using NexmarkFlink.utils;
using System.Collections.Generic;

namespace PublicTests.utils
{
    public class NexmarkGlobalConfigurationPublicTests
    {
        [Fact]
        public void TestGlobalParameterLoadingOverrides()
        {
            var cfg = NexmarkGlobalConfiguration.LoadGlobalConfiguration("src/main/resources/conf");
            Assert.Null(cfg.GetValueOrDefault("nonexistent_override_key"));
        }
    }
}
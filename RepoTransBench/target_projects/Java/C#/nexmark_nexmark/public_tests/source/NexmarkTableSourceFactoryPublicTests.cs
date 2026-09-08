using System;
using Xunit;
using NexmarkFlink.source;

namespace PublicTests.source
{
    public class NexmarkTableSourceFactoryPublicTests
    {
        [Fact]
        public void TestFactoryClassType()
        {
            var factory = new NexmarkTableSourceFactory();
            Assert.IsType<NexmarkTableSourceFactory>(factory);
        }

        [Fact]
        public void TestFactoryToStringNotNull()
        {
            var factory = new NexmarkTableSourceFactory();
            Assert.NotNull(factory.ToString());
        }
    }
}
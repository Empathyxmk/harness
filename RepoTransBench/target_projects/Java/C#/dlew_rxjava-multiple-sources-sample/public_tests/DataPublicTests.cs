using System;
using Xunit;
using MultipleSourcesSample;

namespace MultipleSourcesSample.PublicTests
{
    public class DataPublicTests
    {
        [Fact]
        public void TestIsUpToDate_whenFreshPublic()
        {
            var data = new Data("public");
            Assert.True(data.IsUpToDate());
        }

        [Fact]
        public void TestIsUpToDate_whenStalePublic()
        {
            var data = new Data("anotherPublic");
            System.Threading.Thread.Sleep((int)Data.STALE_MS + 200);
            Assert.False(data.IsUpToDate());
        }

        [Fact]
        public void TestValueAndTimestampPublic()
        {
            var data = new Data("differentSample");
            Assert.Equal("differentSample", data.value);
            Assert.True(data.timestamp <= DateTimeOffset.UtcNow.ToUnixTimeMilliseconds());
        }
    }
}
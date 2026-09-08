using System;
using Xunit;
using MultipleSourcesSample;

namespace MultipleSourcesSample.Tests
{
    public class DataTests
    {
        [Fact]
        public void TestIsUpToDate_whenFresh()
        {
            var data = new Data("test");
            Assert.True(data.IsUpToDate());
        }

        [Fact]
        public void TestIsUpToDate_whenStale()
        {
            var data = new Data("test");
            System.Threading.Thread.Sleep((int)Data.STALE_MS + 100);
            Assert.False(data.IsUpToDate());
        }

        [Fact]
        public void TestValueAndTimestamp()
        {
            var data = new Data("sample");
            Assert.Equal("sample", data.value);
            Assert.True(data.timestamp <= DateTimeOffset.UtcNow.ToUnixTimeMilliseconds());
        }
    }
}
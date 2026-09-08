using System;
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Original
{
    public class TimeProviderTests
    {
        [Fact]
        public void TestGetDateReturnsNow()
        {
            var provider = new TimeProvider();
            var before = DateTime.UtcNow;
            var result = provider.GetDate();
            var after = DateTime.UtcNow;

            Assert.True(result >= before && result <= after);
        }

        [Fact]
        public void TestNowReturnsCurrentTime()
        {
            var provider = new TimeProvider();
            long before = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            long now = provider.Now();
            long after = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            Assert.True(now >= before && now <= after);
        }
    }
}
using System;
using Xunit;

namespace LatencyUtils.Tests.Public
{
    public class TimeServicesPublicTests
    {
        [Fact]
        public void TestNanoTimeAndForward()
        {
            long start = TimeServices.NanoTime();
            TimeServices.MoveTimeForwardMsec(16);
            long end = TimeServices.NanoTime();
            Assert.Equal(start + 16_000_000, end);
        }
    }
}
using System;
using Xunit;

namespace LatencyUtils.Tests.Original
{
    public class TimeServicesTests
    {
        [Fact]
        public void TestNanoTimeAndMillisStatic()
        {
            long n1 = TimeServices.NanoTime();
            long m1 = TimeServices.CurrentTimeMillis();
            Assert.True(n1 > 0);
            Assert.True(m1 > 0);
        }
    }
}
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class SmsRadarServicePublicTests
    {
        [Fact]
        public void TestStubPublicDifferentData()
        {
            var service = new SmsRadarService();
            Assert.NotNull(service);
        }
    }
}
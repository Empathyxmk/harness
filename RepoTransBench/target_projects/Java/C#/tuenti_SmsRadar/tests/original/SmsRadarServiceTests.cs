using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Original
{
    public class SmsRadarServiceTests
    {
        [Fact]
        public void TestStubPublicDifferentData()
        {
            var service = new SmsRadarService();
            Assert.NotNull(service);
        }
    }
}
using System.Threading;
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class TimeProviderPublicTests
    {
        [Fact]
        public void TestEpochTime()
        {
            var tp = new TimeProvider();
            long time = tp.GetCurrentTimeMillis();
            Assert.True(time >= 0);
        }

        [Fact]
        public void TestTimeHasAdvanced()
        {
            var tp = new TimeProvider();
            long before = tp.GetCurrentTimeMillis();
            Thread.Sleep(7);
            long after = tp.GetCurrentTimeMillis();
            Assert.True(after > before);
        }
    }
}
using Xunit;
using System.Threading;

namespace OriginalTests
{
    public class ScheduledTest
    {
        [Fact]
        public void TestScheduledRunnable()
        {
            var task = new Thread(() => { });
            var scheduled = new ProjectName.Scheduled(task, 1000L);
            Assert.Equal(1000L, scheduled.Delay);
            scheduled.Delay = 500L;
            Assert.Equal(500L, scheduled.Delay);
        }
    }
}
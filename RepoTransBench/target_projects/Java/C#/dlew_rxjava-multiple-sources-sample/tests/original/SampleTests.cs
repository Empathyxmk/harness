using System.Threading;
using Xunit;
using MultipleSourcesSample;

namespace MultipleSourcesSample.Tests
{
    public class SampleTests
    {
        [Fact]
        public void TestSleep_noInterrupt()
        {
            // Should complete without exception
            Sample.Sleep(10);
        }

        [Fact]
        public void TestSleep_withInterrupt()
        {
            var thread = new Thread(() => {
                Sample.Sleep(1000L);
            });
            thread.Start();
            thread.Interrupt();
            thread.Join(200);
            // No assertion, but method should handle interruption gracefully
        }
    }
}
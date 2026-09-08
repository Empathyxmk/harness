using System.Threading;
using Xunit;

namespace PublicTests
{
    public class LockPerformancePublicTest
    {
        [Fact]
        public void TestReentrantLockLowContention()
        {
            object lockObj = new object();
            int sum = 0;
            int N = 50; // Different from original value
            for (int i = 0; i < N; i++)
            {
                lock (lockObj)
                {
                    sum += i;
                }
            }

            Assert.True(sum > 0);
        }
    }
}
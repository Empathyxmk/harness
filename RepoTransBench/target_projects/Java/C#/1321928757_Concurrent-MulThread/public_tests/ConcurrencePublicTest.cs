using System;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace PublicTests
{
    public class ConcurrencePublicTest
    {
        [Fact]
        public void TestLowerConcurrency()
        {
            int nThreads = 5;
            int nTasks = 20;
            int increments = 10;
            int expected = nTasks * increments;
            int total = 0;
            object lockObj = new object();

            using (var ready = new CountdownEvent(nTasks))
            using (var done = new CountdownEvent(nTasks))
            {
                for (int i = 0; i < nTasks; i++)
                {
                    Task.Run(() =>
                    {
                        ready.Signal();
                        ready.Wait();
                        for (int j = 0; j < increments; j++)
                        {
                            lock (lockObj) { total++; }
                        }
                        done.Signal();
                    });
                }
                done.Wait();
            }

            Assert.Equal(expected, total);
        }
    }
}
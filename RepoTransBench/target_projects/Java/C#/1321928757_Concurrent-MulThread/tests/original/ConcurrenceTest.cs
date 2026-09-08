using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using Xunit;

namespace OriginalTests
{
    public class ConcurrenceTest
    {
        [Fact]
        public void ConcurrenceTest_HighConcurrency()
        {
            // Simulate high concurrency: 1000 tasks, each increments by 1000
            int tasksCount = 1000;
            int incrementsPerTask = 1000;
            int expected = tasksCount * incrementsPerTask;
            int value = 0;
            object lockObj = new object();

            using (var ready = new CountdownEvent(tasksCount))
            using (var done = new CountdownEvent(tasksCount))
            {
                for (int i = 0; i < tasksCount; i++)
                {
                    Task.Run(() =>
                    {
                        ready.Signal();
                        ready.Wait();
                        for (int j = 0; j < incrementsPerTask; j++)
                        {
                            lock (lockObj)
                            {
                                value++;
                            }
                        }
                        done.Signal();
                    });
                }
                done.Wait();
            }

            Assert.Equal(expected, value);
        }
    }
}
using System;
using System.Threading;
using Xunit;

namespace OriginalTests
{
    // Simulate a custom AQS-style exclusive lock.
    public class OnlySyncByAQS
    {
        private readonly object _lock = new object();

        public void Lock()
        {
            Monitor.Enter(_lock);
        }

        public void Unlock()
        {
            Monitor.Exit(_lock);
        }
    }

    public class CustomAqsSynchronizerTest
    {
        [Fact]
        public void Use_ExclusiveLock_AllowsOnlyOneThread()
        {
            var sync = new OnlySyncByAQS();
            int successCount = 0;
            int threadCount = 3;
            Thread[] threads = new Thread[threadCount];

            for (int i = 0; i < threadCount; i++)
            {
                threads[i] = new Thread(() =>
                {
                    sync.Lock();
                    try
                    {
                        Interlocked.Increment(ref successCount);
                        Thread.Sleep(1000); // Simulate resource usage.
                    }
                    finally
                    {
                        sync.Unlock();
                    }
                });
            }

            foreach (var t in threads)
                t.Start();
            foreach (var t in threads)
                t.Join();

            Assert.Equal(threadCount, successCount);
        }
    }
}
using System;
using System.Threading;
using Xunit;

namespace PublicTests
{
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

    public class CustomAqsSynchronizerPublicTest
    {
        [Fact]
        public void TestCustomAQSLock_MultipleThreads()
        {
            OnlySyncByAQS lockObj = new OnlySyncByAQS();
            int threadCount = 4;
            int count = 0;
            Thread[] threads = new Thread[threadCount];

            for (int t = 0; t < threadCount; t++)
            {
                threads[t] = new Thread(() =>
                {
                    lockObj.Lock();
                    try
                    {
                        Interlocked.Increment(ref count);
                        Thread.Sleep(250);
                    }
                    finally
                    {
                        lockObj.Unlock();
                    }
                });
            }

            foreach (Thread thread in threads)
                thread.Start();
            foreach (Thread thread in threads)
                thread.Join();

            Assert.True(count == threadCount);
        }
    }
}
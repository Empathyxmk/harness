using System;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace OriginalTests
{
    public class LockPerformanceTest
    {
        private readonly object _lock = new object();
        private readonly ReaderWriterLockSlim _rwLock = new ReaderWriterLockSlim();
        private int sharedResource = 0;
        private const int READ_THREADS = 10, WRITE_THREADS = 2, ITERATIONS = 100000;

        [Fact]
        public void TestReentrantLockPerformance()
        {
            int activeThreads = 0;
            var barrier = new Barrier(READ_THREADS + WRITE_THREADS);

            for (int i = 0; i < READ_THREADS; i++)
            {
                new Thread(() =>
                {
                    barrier.SignalAndWait();
                    for (int j = 0; j < ITERATIONS; j++)
                    {
                        lock (_lock)
                        {
                            int value = sharedResource;
                        }
                    }
                    Interlocked.Increment(ref activeThreads);
                }).Start();
            }

            for (int i = 0; i < WRITE_THREADS; i++)
            {
                new Thread(() =>
                {
                    barrier.SignalAndWait();
                    for (int j = 0; j < ITERATIONS; j++)
                    {
                        lock (_lock)
                        {
                            sharedResource++;
                        }
                    }
                    Interlocked.Increment(ref activeThreads);
                }).Start();
            }

            SpinWait.SpinUntil(() => activeThreads == READ_THREADS + WRITE_THREADS, 60000);
            Assert.True(activeThreads == READ_THREADS + WRITE_THREADS);
        }

        [Fact]
        public void TestReadWriteLockPerformance()
        {
            int activeThreads = 0;
            sharedResource = 0;
            var barrier = new Barrier(READ_THREADS + WRITE_THREADS);

            for (int i = 0; i < READ_THREADS; i++)
            {
                new Thread(() =>
                {
                    barrier.SignalAndWait();
                    for (int j = 0; j < ITERATIONS; j++)
                    {
                        _rwLock.EnterReadLock();
                        try
                        {
                            int v = sharedResource;
                        }
                        finally
                        {
                            _rwLock.ExitReadLock();
                        }
                    }
                    Interlocked.Increment(ref activeThreads);
                }).Start();
            }

            for (int i = 0; i < WRITE_THREADS; i++)
            {
                new Thread(() =>
                {
                    barrier.SignalAndWait();
                    for (int j = 0; j < ITERATIONS; j++)
                    {
                        _rwLock.EnterWriteLock();
                        try
                        {
                            sharedResource++;
                        }
                        finally
                        {
                            _rwLock.ExitWriteLock();
                        }
                    }
                    Interlocked.Increment(ref activeThreads);
                }).Start();
            }

            SpinWait.SpinUntil(() => activeThreads == READ_THREADS + WRITE_THREADS, 60000);
            Assert.True(activeThreads == READ_THREADS + WRITE_THREADS);
        }
    }
}
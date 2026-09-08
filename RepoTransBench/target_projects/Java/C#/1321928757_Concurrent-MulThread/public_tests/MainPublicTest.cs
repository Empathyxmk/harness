using System;
using System.Threading;
using System.Collections.Generic;
using Xunit;

namespace PublicTests
{
    // Dummy ThreadPool implementation for test demonstration.
    public class DummyThreadPool
    {
        private readonly int _coreSize;
        private readonly int _maxQueue;
        private readonly Queue<Thread> _threads = new Queue<Thread>();

        public DummyThreadPool(int coreSize, int maxQueue)
        {
            _coreSize = coreSize;
            _maxQueue = maxQueue;
        }

        public void Execute(Action action)
        {
            var thread = new Thread(new ThreadStart(action));
            _threads.Enqueue(thread);
            thread.Start();
        }

        public void Shutdown()
        {
            foreach (var t in _threads)
            {
                if (t.IsAlive)
                    t.Join();
            }
        }

        public bool IsTerminated
        {
            get
            {
                foreach (var t in _threads)
                {
                    if (t.IsAlive)
                        return false;
                }
                return true;
            }
        }
    }

    public class MainPublicTest
    {
        [Fact]
        public void PublicThreadPoolTest()
        {
            int sum = 0;
            var pool = new DummyThreadPool(coreSize: 2, maxQueue: 3);
            int numberOfTasks = 7;
            object lockObj = new object();

            for (int i = 0; i < numberOfTasks; i++)
            {
                int ix = i;
                pool.Execute(() =>
                {
                    lock (lockObj)
                    {
                        sum += ix;
                    }
                });
            }
            pool.Shutdown();

            int expected = 0;
            for (int i = 0; i < numberOfTasks; i++)
                expected += i;

            Assert.Equal(expected, sum);
        }
    }
}
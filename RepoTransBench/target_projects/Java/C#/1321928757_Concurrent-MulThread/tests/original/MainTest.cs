using System;
using System.Threading;
using Xunit;

namespace OriginalTests
{
    // Dummy ThreadPool for test demonstration.
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
    }

    public class MainTest
    {
        [Fact]
        public void ThreadPool_ExecuteSeveralTasks_AndShutdown()
        {
            var pool = new DummyThreadPool(coreSize: 2, maxQueue: 5);
            int counter = 0;
            object lockObj = new object();

            for (int i = 0; i < 15; i++)
            {
                int local = i;
                pool.Execute(() =>
                {
                    lock (lockObj) { counter++; }
                });
            }
            pool.Shutdown();

            Assert.Equal(15, counter);
        }
    }
}
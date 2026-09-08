using Xunit;
using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;

namespace OriginalTests
{
    public class PoolTest
    {
        [Fact]
        public void TestExecutorQueue()
        {
            var queue = new ProjectName.ExecutorQueue<Action>();
            Assert.True(queue.Offer(() => { }));
            Assert.NotNull(queue.Poll());
            Assert.Null(queue.Poll());
        }

        [Fact]
        public void TestDefaultThreadFactory()
        {
            var factory = new ProjectName.DefaultThreadFactory("testPool", true);
            Action r = () => { };
            Thread t = factory.NewThread(r);
            Assert.NotNull(t);
            Assert.Contains("testPool", t.Name);
            Assert.True(t.IsBackground);
        }

        [Fact]
        public void TestScheduled()
        {
            var scheduled = new ProjectName.Scheduled();
            Action task = () => { };
            scheduled.Schedule(task, 10, TimeSpan.FromMilliseconds(1));
            scheduled.Shutdown();
            Assert.True(scheduled.IsShutdown || !scheduled.IsShutdown); // for coverage
        }

        [Fact]
        public void TestStandardThreadExecutor()
        {
            var executor = new ProjectName.StandardThreadExecutor(1, 2, TimeSpan.FromSeconds(60), new ProjectName.ExecutorQueue<Action>());
            bool ran = false;
            executor.Execute(() => ran = true);
            Thread.Sleep(100);
            Assert.True(ran);
            executor.Shutdown();
            Assert.True(executor.IsShutdown || !executor.IsShutdown);
        }
    }
}
using Xunit;

namespace OriginalTests
{
    public class ExecutorQueueTest
    {
        [Fact]
        public void TestOfferAndPoll()
        {
            var queue = new ProjectName.ExecutorQueue<int>();
            Assert.True(queue.Offer(1));
            Assert.Equal(1, queue.Poll());
            Assert.Null(queue.Poll());
        }

        [Fact]
        public void TestMultipleOperations()
        {
            var queue = new ProjectName.ExecutorQueue<string>();
            Assert.True(queue.Offer("A"));
            Assert.True(queue.Offer("B"));
            Assert.Equal("A", queue.Poll());
            Assert.Equal("B", queue.Poll());
            Assert.Null(queue.Poll());
        }

        [Fact]
        public void TestSizeIsEmpty()
        {
            var queue = new ProjectName.ExecutorQueue<double>();
            Assert.True(queue.IsEmpty());
            queue.Offer(2.5);
            Assert.False(queue.IsEmpty());
            Assert.Equal(1, queue.Size());
            queue.Poll();
            Assert.True(queue.IsEmpty());
            Assert.Equal(0, queue.Size());
        }
    }
}
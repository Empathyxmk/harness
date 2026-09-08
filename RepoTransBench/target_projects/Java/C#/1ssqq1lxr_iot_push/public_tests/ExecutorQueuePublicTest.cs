using Xunit;

namespace PublicTests
{
    public class ExecutorQueuePublicTest
    {
        [Fact]
        public void TestOfferAndPollWithDifferentValues()
        {
            var queue = new ProjectName.ExecutorQueue<int>();
            Assert.True(queue.Offer(99));
            Assert.Equal(99, queue.Poll());
            Assert.Null(queue.Poll());
        }

        [Fact]
        public void TestMultipleOperationsWithStrings()
        {
            var queue = new ProjectName.ExecutorQueue<string>();
            Assert.True(queue.Offer("X"));
            Assert.True(queue.Offer("Y"));
            Assert.Equal("X", queue.Poll());
            Assert.Equal("Y", queue.Poll());
            Assert.Null(queue.Poll());
        }

        [Fact]
        public void TestSizeIsEmptyWithDifferentType()
        {
            var queue = new ProjectName.ExecutorQueue<double>();
            Assert.True(queue.IsEmpty());
            queue.Offer(7.7);
            Assert.False(queue.IsEmpty());
            Assert.Equal(1, queue.Size());
            queue.Poll();
            Assert.True(queue.IsEmpty());
            Assert.Equal(0, queue.Size());
        }
    }
}
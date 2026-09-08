using Xunit;

namespace PublicTests.Sequence
{
    public class ZkDistributedSequencePublicTests
    {
        [Fact]
        public void TestIncrementSequencePublic()
        {
            long baseVal = 1000L;
            long incremented = baseVal + 11L;
            Assert.Equal(1011L, incremented);
        }

        [Fact]
        public void TestSequenceWrapAroundPublic()
        {
            long maxValue = 50L;
            long value = (maxValue + 8) % maxValue;
            Assert.Equal(8L, value);
        }
    }
}
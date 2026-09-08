using Xunit;
using AllenDowney.ThinkJavaCode;

namespace OriginalTests.Ap01
{
    public class SeriesTest
    {
        [Fact]
        public void TestFibonacci()
        {
            Assert.Equal(1, Series.Fibonacci(1));
            Assert.Equal(1, Series.Fibonacci(2));
            Assert.Equal(2, Series.Fibonacci(3));
        }
    }
}
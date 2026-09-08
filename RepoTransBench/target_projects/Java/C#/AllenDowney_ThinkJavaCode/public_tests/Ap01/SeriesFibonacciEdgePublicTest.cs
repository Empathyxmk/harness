using Xunit;
using AllenDowney.ThinkJavaCode;

namespace PublicTests.Ap01
{
    public class SeriesFibonacciEdgePublicTest
    {
        [Fact]
        public void TestFibonacciLow()
        {
            Assert.Equal(13, Series.Fibonacci(7));
            Assert.Equal(21, Series.Fibonacci(8));
        }

        [Fact]
        public void TestFibonacciHighDifferentInputs()
        {
            Assert.Equal(55, Series.Fibonacci(10));
            Assert.Equal(89, Series.Fibonacci(11));
            Assert.Equal(144, Series.Fibonacci(12));
        }

        [Fact]
        public void TestFibonacciEdge()
        {
            Assert.Equal(1, Series.Fibonacci(1));
            Assert.Equal(1, Series.Fibonacci(2));
        }
    }
}
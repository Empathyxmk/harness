using Xunit;
using AllenDowney.ThinkJavaCode;

namespace OriginalTests.Ap01
{
    public class SeriesFibonacciEdgeTest
    {
        [Fact]
        public void TestFibonacciZeroAndNegative()
        {
            // Defensive: Accept any error for bad/invalid input
            Assert.ThrowsAny<System.Exception>(() => Series.Fibonacci(0));
            Assert.ThrowsAny<System.Exception>(() => Series.Fibonacci(-5));
        }
    }
}
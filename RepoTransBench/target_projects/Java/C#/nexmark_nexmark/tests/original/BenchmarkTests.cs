using System;
using Xunit;
using NexmarkFlink;

namespace OriginalTests
{
    public class BenchmarkTests
    {
        [Fact]
        public void TestMainWithNoArgsThrowsRuntimeException()
        {
            var ex = Assert.Throws<Exception>(() => Benchmark.Main(new string[] { }));
            Assert.Contains("Usage", ex.Message);
        }
    }
}
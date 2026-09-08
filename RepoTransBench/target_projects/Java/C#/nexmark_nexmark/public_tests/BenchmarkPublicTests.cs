using System;
using Xunit;
using NexmarkFlink;

namespace PublicTests
{
    public class BenchmarkPublicTests
    {
        [Fact]
        public void TestMainWithNullArgsThrowsRuntimeException()
        {
            var ex = Assert.Throws<Exception>(() => Benchmark.Main(null));
            Assert.Contains("usage", ex.Message, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void TestMainWithInvalidArgsThrowsParseExceptionOrRuntime()
        {
            var ex = Assert.ThrowsAny<Exception>(() => Benchmark.Main(new string[] { "--foo" }));
            Assert.NotNull(ex.Message);
        }
    }
}
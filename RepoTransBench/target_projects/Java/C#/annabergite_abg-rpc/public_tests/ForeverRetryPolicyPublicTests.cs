using System;
using Xunit;

namespace AnnabergiteAbgRpc.PublicTests
{
    public class ForeverRetryPolicyPublicTests
    {
        [Fact]
        public void TestShouldRetryAfterDifferentAttempt()
        {
            int attempt = 42;
            var policy = new ForeverRetryPolicy();
            bool shouldRetry = policy.ShouldRetry(attempt);
            Assert.True(shouldRetry);
        }
        public class ForeverRetryPolicy
        {
            public bool ShouldRetry(int attempt) => true;
        }
    }
}
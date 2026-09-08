using System;
using Xunit;

namespace AnnabergiteAbgRpc.Tests.Original
{
    public class ForeverRetryPolicyTests
    {
        [Fact]
        public void TestConstructorAndAllowValid()
        {
            var policy = new ForeverRetryPolicy(10, 100);
            Assert.NotNull(policy);

            RetrySleeper sleeper = (time, unit) => { /* sleep simulation */ };
            Assert.True(policy.AllowRetry(0, 0, sleeper));
            Assert.True(policy.AllowRetry(5, 0, sleeper));
            Assert.True(policy.AllowRetry(-1, 0, sleeper));
        }

        [Fact]
        public void TestAllowRetryInterrupted()
        {
            var policy = new ForeverRetryPolicy(10, 100);
            // Custom sleeper to throw InterruptedException (simulate with exception catching)
            RetrySleeper sleeper = (time, unit) => { throw new OperationCanceledException(); };
            Assert.False(policy.AllowRetry(0, 0, sleeper));
        }

        [Fact]
        public void TestConstructorInvalidArguments()
        {
            Assert.Throws<ArgumentException>(() => new ForeverRetryPolicy(-1, 10));
            Assert.Throws<ArgumentException>(() => new ForeverRetryPolicy(1, 0));
            Assert.Throws<ArgumentException>(() => new ForeverRetryPolicy(100, 10));
        }
    }

    // Simulated classes for ForeverRetryPolicy and RetrySleeper
    public delegate void RetrySleeper(long time, string unit);

    public class ForeverRetryPolicy
    {
        public long BaseSleepTimeMs { get; }
        public long MaxSleepMs { get; }

        public ForeverRetryPolicy(long baseSleepTimeMs = 1000, long maxSleepMs = 10000)
        {
            if (baseSleepTimeMs < 0 || maxSleepMs <= 0 || maxSleepMs < baseSleepTimeMs)
                throw new ArgumentException();
            BaseSleepTimeMs = baseSleepTimeMs;
            MaxSleepMs = maxSleepMs;
        }
        public bool AllowRetry(int retryCount, long elapsedTimeMs, RetrySleeper sleeper)
        {
            try
            {
                sleeper?.Invoke(BaseSleepTimeMs, "ms");
                return true;
            }
            catch (OperationCanceledException)
            {
                return false;
            }
        }
    }
}
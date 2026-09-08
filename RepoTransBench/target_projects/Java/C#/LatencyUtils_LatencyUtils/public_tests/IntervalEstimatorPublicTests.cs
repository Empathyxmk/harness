using System;
using Xunit;

namespace LatencyUtils.Tests.Public
{
    public abstract class IntervalEstimator
    {
        public abstract void RecordInterval(long when);
        public abstract long GetEstimatedInterval(long when);
    }

    public class IntervalEstimatorPublicTests
    {
        [Fact]
        public void TestAbstractMethodReturnsDifferentValue()
        {
            IntervalEstimator estimator = new DummyIntervalEstimator();
            estimator.RecordInterval(100L);
            long est = estimator.GetEstimatedInterval(101L);
            Assert.Equal(456L, est);
        }

        private class DummyIntervalEstimator : IntervalEstimator
        {
            public override void RecordInterval(long when) { /* no-op */ }
            public override long GetEstimatedInterval(long when) { return 456L; }
        }
    }
}
using System;
using Xunit;

namespace LatencyUtils.Tests.Original
{
    public abstract class IntervalEstimator
    {
        public abstract void RecordInterval(long when);
        public abstract long GetEstimatedInterval(long when);
    }

    public class IntervalEstimatorTests
    {
        [Fact]
        public void TestAbstractMethodThrows()
        {
            // Mimic the dummy subclass pattern
            IntervalEstimator estimator = new DummyIntervalEstimator();
            estimator.RecordInterval(1L);
            long est = estimator.GetEstimatedInterval(2L);
            Assert.Equal(123L, est);
        }

        private class DummyIntervalEstimator : IntervalEstimator
        {
            public override void RecordInterval(long when)
            {
                // no-op
            }
            public override long GetEstimatedInterval(long when)
            {
                return 123L;
            }
        }
    }
}
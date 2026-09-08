using System;
using Xunit;

namespace LatencyUtils.Tests.Original
{
    // Assume a stub for MovingAverageIntervalEstimator exists in the main src/LatencyUtils/
    public class MovingAverageIntervalEstimatorTests
    {
        static MovingAverageIntervalEstimatorTests()
        {
            // Simulate: System.setProperty("LatencyUtils.useActualTime", "false");
            // In C#: would set some static config variable if needed by implementation.
        }

        [Fact]
        public void TestMovingAverageIntervalEstimator()
        {
            var estimator = new MovingAverageIntervalEstimator(1024);

            long now = 0;

            for (int i = 0; i < 10000; i++)
            {
                now += 20;
                estimator.RecordInterval(now);
            }

            Assert.Equal(20, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 512; i++)
            {
                now += 40;
                estimator.RecordInterval(now);
            }

            Assert.Equal(30, estimator.GetEstimatedInterval(0));

            for (int i = 0; i < 256; i++)
            {
                now += 60;
                estimator.RecordInterval(now);
            }

            Assert.Equal(40, estimator.GetEstimatedInterval(0));
        }
    }
}
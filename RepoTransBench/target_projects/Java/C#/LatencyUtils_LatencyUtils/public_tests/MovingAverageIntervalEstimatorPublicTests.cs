using System;
using Xunit;

namespace LatencyUtils.Tests.Public
{
    public class MovingAverageIntervalEstimatorPublicTests
    {
        static MovingAverageIntervalEstimatorPublicTests()
        {
            // Simulates System.setProperty("LatencyUtils.useActualTime", "false");
        }

        [Fact]
        public void TestMovingAverageIntervalEstimatorPublic()
        {
            var estimator = new MovingAverageIntervalEstimator(512);

            long now = 0;
            for (int i = 0; i < 8000; i++)
            {
                now += 25;
                estimator.RecordInterval(now);
            }

            Assert.Equal(25, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 400; i++)
            {
                now += 50;
                estimator.RecordInterval(now);
            }

            Assert.Equal(37, estimator.GetEstimatedInterval(0));

            for (int i = 0; i < 200; i++)
            {
                now += 80;
                estimator.RecordInterval(now);
            }

            Assert.Equal(53, estimator.GetEstimatedInterval(0));
        }
    }
}
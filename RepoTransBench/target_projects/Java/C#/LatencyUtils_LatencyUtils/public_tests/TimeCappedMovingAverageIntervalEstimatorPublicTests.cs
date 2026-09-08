using System;
using System.Threading;
using Xunit;

namespace LatencyUtils.Tests.Public
{
    public class TimeCappedMovingAverageIntervalEstimatorPublicTests
    {
        static TimeCappedMovingAverageIntervalEstimatorPublicTests()
        {
            // Simulates System.setProperty("LatencyUtils.useActualTime", "false");
        }

        [Fact]
        public void TestWindowBehaviorPublic()
        {
            var pauseDetector = new MyArtificialPauseDetectorPublic();
            var estimator = new TimeCappedMovingAverageIntervalEstimator(16, 500_000_000L, pauseDetector);

            Thread.Sleep(10); // Sleep 10ms

            long now = 0;
            for (int i = 0; i < 5000; i++)
            {
                now += 15;
                estimator.RecordInterval(now);
            }
            Assert.Equal(15, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 8; i++)
            {
                now += 30;
                estimator.RecordInterval(now);
            }
            Assert.Equal(22, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 4; i++)
            {
                now += 60;
                estimator.RecordInterval(now);
            }
            Assert.Equal(32, estimator.GetEstimatedInterval(now));

            pauseDetector.RecordPause(600_000_000L, now + 600_000_000L);
            now += 600_000_000L;
            Thread.Sleep(10);

            Assert.Equal(32, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 4; i++)
            {
                estimator.RecordInterval(now);
                now += 60;
            }
            Assert.Equal(47, estimator.GetEstimatedInterval(now));

            now = 1_600_000_000L;
            Assert.Equal(long.MaxValue, estimator.GetEstimatedInterval(now));

            estimator.RecordInterval(now);

            for (int i = 0; i < 8; i++)
            {
                now += 10;
                estimator.RecordInterval(now);
            }
            Assert.Equal(10, estimator.GetEstimatedInterval(now));

            pauseDetector.RecordPause(700_000_000L, 2_001_000_000L);
            now = 2_001_000_000L;
            Thread.Sleep(10);

            estimator.RecordInterval(now);

            for (int i = 0; i < 8; i++)
            {
                now += 15;
                estimator.RecordInterval(now);
            }
            now = 2_001_000_000L + (10 * 1_000_000);

            Assert.Equal(1_000_000, estimator.GetEstimatedInterval(now));

            now = 2_700_000_000L;
            Assert.Equal(long.MaxValue, estimator.GetEstimatedInterval(now));
        }

        public class MyArtificialPauseDetectorPublic : PauseDetector
        {
            public volatile long LatestPauseEndTime = 0;
            public void RecordPause(long length, long when)
            {
                NotifyListeners(length, when);
                LatestPauseEndTime = when;
            }
        }
    }
}
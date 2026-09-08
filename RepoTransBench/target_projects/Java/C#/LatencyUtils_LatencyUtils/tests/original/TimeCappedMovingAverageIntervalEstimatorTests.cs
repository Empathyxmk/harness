using System;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace LatencyUtils.Tests.Original
{
    // Assume main classes exist in main src.
    public class TimeCappedMovingAverageIntervalEstimatorTests
    {
        static TimeCappedMovingAverageIntervalEstimatorTests()
        {
            // Equivalent of: System.setProperty("LatencyUtils.useActualTime", "false");
        }

        [Fact]
        public void TestWindowBehavior()
        {
            var pauseDetector = new MyArtificialPauseDetector();
            var estimator = new TimeCappedMovingAverageIntervalEstimator(32, 1_000_000_000L, pauseDetector);

            // Wait for listener registration
            Thread.Sleep(TimeSpan.FromMilliseconds(20));

            long now = 0;
            for (int i = 0; i < 10000; i++)
            {
                now += 20;
                estimator.RecordInterval(now);
            }
            Assert.Equal(20, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 16; i++)
            {
                now += 40;
                estimator.RecordInterval(now);
            }
            Assert.Equal(30, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 8; i++)
            {
                now += 60;
                estimator.RecordInterval(now);
            }
            Assert.Equal(40, estimator.GetEstimatedInterval(now));

            pauseDetector.RecordPause(1_500_000_000L, now + 1_500_000_000L);
            now += 1_500_000_000L;
            Thread.Sleep(TimeSpan.FromMilliseconds(20));

            Assert.Equal(40, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 8; i++)
            {
                estimator.RecordInterval(now);
                now += 60;
            }
            Assert.Equal(50, estimator.GetEstimatedInterval(now));

            now = 4_000_000_000L;
            Assert.Equal(long.MaxValue, estimator.GetEstimatedInterval(now));

            estimator.RecordInterval(now);
            for (int i = 0; i < 16; i++)
            {
                now += 20;
                estimator.RecordInterval(now);
            }
            Assert.Equal(20, estimator.GetEstimatedInterval(now));

            pauseDetector.RecordPause(1_500_000_000L, 5_501_000_000L);
            now = 5_501_000_000L;
            Thread.Sleep(TimeSpan.FromMilliseconds(20));

            estimator.RecordInterval(now);
            for (int i = 0; i < 14; i++)
            {
                now += 40;
                estimator.RecordInterval(now);
            }
            now = 5_501_000_000L + (30 * 1_000_000);

            Assert.Equal(1_000_000, estimator.GetEstimatedInterval(now));

            pauseDetector.RecordPause(1_500_000_000L, 7_100_000_000L);
            now = 7_100_000_000L;
            Thread.Sleep(TimeSpan.FromMilliseconds(20));
            now = 7_100_000_000L + (21 * 10_000_000);

            Assert.Equal(10_000_000, estimator.GetEstimatedInterval(now));

            for (int i = 0; i < 6; i++)
            {
                now += 40;
                estimator.RecordInterval(now);
            }
            now = 8_001_000_000L;

            Assert.Equal(50_000_000, estimator.GetEstimatedInterval(now));
            estimator.RecordInterval(now);

            now = 8_001_000_040L;
            Assert.Equal(50_000_000, estimator.GetEstimatedInterval(now));

            now = 9_001_000_000L;
            Assert.Equal(long.MaxValue, estimator.GetEstimatedInterval(now));

            now = 12_000_000_000L;
            estimator.RecordInterval(now);
            estimator.RecordInterval(now);

            pauseDetector.RecordPause(1_500_000_000L, 13_500_000_000L);
            now = 13_500_000_000L;
            Thread.Sleep(TimeSpan.FromMilliseconds(20));

            pauseDetector.RecordPause(1_500_000_000L, 15_500_000_000L);
            now = 15_500_000_000L;
            Thread.Sleep(TimeSpan.FromMilliseconds(20));

            Assert.Equal(500_000_000, estimator.GetEstimatedInterval(now));

            now = 16_600_000_000L;
            Assert.Equal(long.MaxValue, estimator.GetEstimatedInterval(now));
        }

        [Fact]
        public void TestToStringOverride()
        {
            var pauseDetector = new MyArtificialPauseDetector();
            var estimator = new TimeCappedMovingAverageIntervalEstimator(1024, 10_000_000_000L, pauseDetector);

            for (int i = 0; i < 2000; i++)
            {
                estimator.RecordInterval(TimeServices.NanoTime());
                TimeServices.MoveTimeForwardMsec(1);
                Thread.Sleep(TimeSpan.FromMilliseconds(0.1));
            }

            TimeServices.MoveTimeForwardMsec(1000);
            Thread.Sleep(TimeSpan.FromMilliseconds(1));

            estimator.GetEstimatedInterval(TimeServices.NanoTime());
            var toString = estimator.ToString();
            // Output for debugging; no assert since just checking not to throw
            // Console.WriteLine("toString():\n" + estimator);
            Assert.False(string.IsNullOrEmpty(toString));
        }

        [Fact]
        public void TestIntervalWithSleeping()
        {
            var pauseDetector = new MyArtificialPauseDetector();
            var estimator = new TimeCappedMovingAverageIntervalEstimator(128, 10_000_000_000L, pauseDetector);

            long startTime = TimeServices.NanoTime();
            for (int i = 0; i < 5; i++)
            {
                estimator.GetEstimatedInterval(TimeServices.NanoTime());
                if (i > 1)
                {
                    Assert.Equal(1_000_000, estimator.GetEstimatedInterval(TimeServices.NanoTime()));
                }
                for (int j = 0; j < 64; j++)
                {
                    TimeServices.MoveTimeForwardMsec(1);
                    Thread.Sleep(TimeSpan.FromMilliseconds(0.1));
                    estimator.RecordInterval(TimeServices.NanoTime());
                }
            }
            long pauseStartTime = TimeServices.NanoTime();
            TimeServices.MoveTimeForwardMsec(500);
            Thread.Sleep(TimeSpan.FromMilliseconds(1));
            long pauseEndTime = TimeServices.NanoTime();
            pauseDetector.RecordPause(pauseEndTime - pauseStartTime, pauseEndTime);

            for (int i = 0; i < 5; i++)
            {
                estimator.GetEstimatedInterval(TimeServices.NanoTime());
                if (i > 1)
                {
                    Assert.Equal(2_000_000, estimator.GetEstimatedInterval(TimeServices.NanoTime()));
                }
                for (int j = 0; j < 64; j++)
                {
                    TimeServices.MoveTimeForwardMsec(2);
                    Thread.Sleep(TimeSpan.FromMilliseconds(0.1));
                    estimator.RecordInterval(TimeServices.NanoTime());
                }
            }
        }

        public class MyArtificialPauseDetector : PauseDetector
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
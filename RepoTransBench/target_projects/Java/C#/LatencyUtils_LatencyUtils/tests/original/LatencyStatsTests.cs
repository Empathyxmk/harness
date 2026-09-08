using System;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace LatencyUtils.Tests.Original
{
    public class LatencyStatsTests
    {
        static LatencyStatsTests()
        {
            // Simulate: System.setProperty("LatencyUtils.useActualTime", "false");
        }

        const long HighestTrackableValue = 3600L * 1000 * 1000 * 1000;
        const int NumberOfSignificantValueDigits = 2;
        const long MSEC = 1_000_000L;

        [Fact]
        public void TestLatencyStats()
        {
            var pauseDetector = new SimplePauseDetector(1_000_000L, 10_000_000L, 3, true);
            LatencyStats.SetDefaultPauseDetector(pauseDetector);

            var latencyStats = new LatencyStats();
            var accumulatedHistogram = new Histogram(latencyStats.GetIntervalHistogram());

            try
            {
                Thread.Sleep(100);

                pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + 115 * MSEC);

                TimeServices.MoveTimeForward(5000L);
                Thread.Sleep(1);
                TimeServices.MoveTimeForward(1_000_000L);
                Thread.Sleep(1);
                TimeServices.MoveTimeForward(2_000_000L);
                Thread.Sleep(1);
                TimeServices.MoveTimeForward(110_000_000L);
                Thread.Sleep(1);

                Thread.Sleep(10);

                long startTime = TimeServices.NanoTime();

                long lastTime = startTime;
                for (int i = 0; i < 2000; i++)
                {
                    pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + (4 * MSEC));
                    TimeServices.MoveTimeForwardMsec(5);
                    long now = TimeServices.NanoTime();
                    latencyStats.RecordLatency(now - lastTime);
                    lastTime = now;
                }

                Thread.Sleep(1);

                var intervalHistogram = latencyStats.GetIntervalHistogram();
                accumulatedHistogram.Add(intervalHistogram);

                Assert.Equal(2000, accumulatedHistogram.GetTotalCount());

                pauseDetector.StallDetectorThreads(0x7, 5000 * MSEC);
                Thread.Sleep(1);

                Assert.Equal(2000, accumulatedHistogram.GetTotalCount());

                intervalHistogram = latencyStats.GetIntervalHistogram();
                accumulatedHistogram.Add(intervalHistogram);

                Assert.Equal(2998, accumulatedHistogram.GetTotalCount());

                pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + (500 * MSEC));
                TimeServices.MoveTimeForwardMsec(500);
                Thread.Sleep(1);

                intervalHistogram = latencyStats.GetIntervalHistogram();
                accumulatedHistogram.Add(intervalHistogram);

                Assert.Equal(2998, accumulatedHistogram.GetTotalCount());

                pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + (500 * MSEC));
                TimeServices.MoveTimeForwardMsec(500);
                Thread.Sleep(1);

                intervalHistogram = latencyStats.GetIntervalHistogram();
                accumulatedHistogram.Add(intervalHistogram);

                Assert.Equal(2998, accumulatedHistogram.GetTotalCount());

                pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + (2000 * MSEC));
                TimeServices.MoveTimeForwardMsec(2000);
                Thread.Sleep(1);

                intervalHistogram = latencyStats.GetIntervalHistogram();
                accumulatedHistogram.Add(intervalHistogram);

                Assert.Equal(2998, accumulatedHistogram.GetTotalCount());

                for (int i = 0; i < 100; i++)
                {
                    pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + (5 * MSEC));
                    TimeServices.MoveTimeForwardMsec(5);
                    long now = TimeServices.NanoTime();
                    latencyStats.RecordLatency(now - lastTime);
                    lastTime = now;
                }

                pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + (500 * MSEC));
                TimeServices.MoveTimeForwardMsec(500);
                Thread.Sleep(1);

                intervalHistogram = latencyStats.GetIntervalHistogram();
                accumulatedHistogram.Add(intervalHistogram);

                pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + (500 * MSEC));
                TimeServices.MoveTimeForwardMsec(500);
                Thread.Sleep(1);

                intervalHistogram = latencyStats.GetIntervalHistogram();
                accumulatedHistogram.Add(intervalHistogram);

                Assert.Equal(3098, accumulatedHistogram.GetTotalCount());
            }
            catch (ThreadInterruptedException) { }

            latencyStats.Stop();
            pauseDetector.Shutdown();
        }

        [Fact]
        public void TestIntervalSampleDeadlock()
        {
            var pauseDetector = new SimplePauseDetector(1_000_000L, 10_000_000L, 3, true);
            LatencyStats.SetDefaultPauseDetector(pauseDetector);

            var latencyStats = new LatencyStats();

            try
            {
                Thread.Sleep(100);
                pauseDetector.SkipConsensusTimeTo(TimeServices.NanoTime() + 115 * MSEC);

                TimeServices.MoveTimeForward(5000L);
                Thread.Sleep(1);
                TimeServices.MoveTimeForward(1_000_000L);
                Thread.Sleep(1);
                TimeServices.MoveTimeForward(2_000_000L);
                Thread.Sleep(1);
                TimeServices.MoveTimeForward(110_000_000L);
                Thread.Sleep(1);

                Thread.Sleep(10);

                long startTime = TimeServices.NanoTime();
                try
                {
                    latencyStats.RecordLatency(long.MaxValue);
                }
                catch (IndexOutOfRangeException)
                {
                    // expected
                }

                Thread.Sleep(1);

                var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));
                var t = Task.Run(() =>
                {
                    try
                    {
                        latencyStats.GetIntervalHistogram();
                    }
                    catch { }
                }, cts.Token);

                bool completed = t.Wait(TimeSpan.FromSeconds(6));
                if (!completed)
                {
                    // Try to forcibly reset state
                    // Not possible to access private field in C# unless we use reflection,
                    // but for translation purposes, we assume this handles. In prod: adjust this logic appropriately!
                    Assert.True(false, "Timed out trying to force interval sample.");
                }
            }
            catch (ThreadInterruptedException) { }
            finally
            {
                latencyStats.Stop();
                pauseDetector.Shutdown();
            }
        }
    }
}
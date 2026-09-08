using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using Xunit;

namespace LatencyUtils.Tests.Original
{
    public class SimplePauseDetectorTests
    {
        static SimplePauseDetectorTests()
        {
            // Simulate: System.setProperty("LatencyUtils.useActualTime", "false");
        }

        [Fact]
        public void TestSimpleSleepingPauseDetectorDetects()
        {
            var detectedPauseLength = new System.Threading.AtomicLong();
            var pauseDetector = new SimplePauseDetector(
                1_000_000L, // 1 msec sleep
                10_000_000L, // 10 msec reporting threshold
                3, // thread count
                true // verbose
            );

            TimeServices.MoveTimeForward(5000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(5000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(1_000_000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(1_000_000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(2_000_000L);
            Thread.Sleep(1);

            var tracker = new PauseTracker(pauseDetector, this, detectedPauseLength);

            try
            {
                Thread.Sleep(100);
                detectedPauseLength.Value = 0;
                Thread.Sleep(100);

                pauseDetector.StallDetectorThreads(0x1, 20_000_000L);
                Thread.Sleep(1);

                pauseDetector.StallDetectorThreads(0x2, 20_000_000L);
                Thread.Sleep(1);

                pauseDetector.StallDetectorThreads(0x4, 20_000_000L);
                Thread.Sleep(1);

                Assert.True(detectedPauseLength.Value == 0);

                detectedPauseLength.Value = 0;
                pauseDetector.StallDetectorThreads(0x7, 20_000_000L);
                Thread.Sleep(1);
                Thread.Sleep(100);

                Assert.True(detectedPauseLength.Value > 10_000_000L);
                if (!TimeServices.UseActualTime)
                {
                    Assert.Equal(19_000_000L, detectedPauseLength.Value);
                }
            }
            catch (ThreadInterruptedException) { }

            tracker.Stop();
            pauseDetector.Shutdown();
        }

        [Fact]
        public void TestSimpleShortSleepingPauseDetectorDetects()
        {
            var detectedPauseLength = new System.Threading.AtomicLong();
            var pauseDetector = new SimplePauseDetector(
                20_000L, // 20 usec sleep
                2_000_000L, // 2 msec reporting threshold
                3,
                true
            );
            TimeServices.MoveTimeForward(5000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(20_000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(20_000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(1_000_000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(2_000_000L);
            Thread.Sleep(1);

            var tracker = new PauseTracker(pauseDetector, this, detectedPauseLength);

            try
            {
                Thread.Sleep(100);
                detectedPauseLength.Value = 0;
                Thread.Sleep(2000);

                Assert.True(detectedPauseLength.Value == 0);
                detectedPauseLength.Value = 0;

                pauseDetector.StallDetectorThreads(0xffff, 3_000_000L);
                Thread.Sleep(50);

                Assert.True(detectedPauseLength.Value > 2_000_000L);

                if (!TimeServices.UseActualTime)
                {
                    Assert.Equal(2_980_000L, detectedPauseLength.Value);
                }
            }
            catch (ThreadInterruptedException) { }

            tracker.Stop();
            pauseDetector.Shutdown();
        }

        [Fact]
        public void TestSimpleSpinningPauseDetectorDetects()
        {
            var detectedPauseLength = new System.Threading.AtomicLong();
            var pauseDetector = new SimplePauseDetector(
                0L, // 0 msec sleep
                50_000L, // 250 usec reporting threshold
                3,
                true
            );
            TimeServices.MoveTimeForward(5000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(5000L);
            Thread.Sleep(1);
            TimeServices.MoveTimeForward(50_000L);
            Thread.Sleep(1);

            var tracker = new PauseTracker(pauseDetector, this, detectedPauseLength);
            try
            {
                Thread.Sleep(1000);
                detectedPauseLength.Value = 0;
                Thread.Sleep(100);

                Assert.True(detectedPauseLength.Value == 0);
                detectedPauseLength.Value = 0;

                pauseDetector.StallDetectorThreads(0x7, 100_000L);
                Thread.Sleep(50);

                Assert.True(detectedPauseLength.Value > 50_000L);
                if (!TimeServices.UseActualTime)
                {
                    Assert.Equal(100_000L, detectedPauseLength.Value);
                }
            }
            catch (ThreadInterruptedException) { }

            tracker.Stop();
            pauseDetector.Shutdown();
        }

        public class PauseTracker : PauseDetectorListener
        {
            private readonly PauseDetector _pauseDetector;
            private readonly System.Threading.AtomicLong _detectedPauseLength;

            public PauseTracker(PauseDetector pauseDetector, object test, System.Threading.AtomicLong detectedPauseLength)
            {
                _pauseDetector = pauseDetector;
                _detectedPauseLength = detectedPauseLength;
                _pauseDetector.AddListener(this);
            }

            public void Stop()
            {
                _pauseDetector.RemoveListener(this);
            }

            public void HandlePauseEvent(long pauseLengthNsec, long pauseEndTimeNsec)
            {
                _detectedPauseLength.Value = pauseLengthNsec;
            }
        }
    }

    // Simple simulation for Java's AtomicLong
    namespace System.Threading
    {
        public class AtomicLong
        {
            private long _value;
            public long Value
            {
                get { return _value; }
                set { _value = value; }
            }
        }
    }
}
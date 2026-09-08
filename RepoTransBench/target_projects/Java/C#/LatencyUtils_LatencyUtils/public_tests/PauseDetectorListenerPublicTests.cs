using System;
using Xunit;

namespace LatencyUtils.Tests.Public
{
    public class PauseDetectorListenerPublicTests
    {
        [Fact]
        public void TestListenerIsCalledWithDifferentArgs()
        {
            bool wasCalled = false;
            var listener = new PauseDetector.Listener((pauseLength, pauseEndTime) =>
            {
                wasCalled = (pauseLength == 777L && pauseEndTime == 5555L);
            });
            var listeners = new[] { listener };
            foreach (var l in listeners)
            {
                l.HandlePauseEvent(777L, 5555L);
            }
            Assert.True(wasCalled);
        }
    }

    public class PauseDetector
    {
        public class Listener
        {
            private readonly Action<long, long> _handlePauseEvent;
            public Listener(Action<long, long> handler)
            {
                _handlePauseEvent = handler;
            }

            public virtual void HandlePauseEvent(long pauseLength, long pauseEndTime)
            {
                _handlePauseEvent(pauseLength, pauseEndTime);
            }
        }
    }
}
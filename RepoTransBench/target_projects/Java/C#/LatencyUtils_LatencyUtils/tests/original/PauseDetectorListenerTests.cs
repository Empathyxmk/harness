using System;
using Xunit;

namespace LatencyUtils.Tests.Original
{
    public interface IPauseDetectorListener
    {
        void HandlePauseEvent(long pauseLength, long pauseEndTime);
    }

    public class PauseDetectorListenerTests
    {
        private class TestListener : IPauseDetectorListener
        {
            public long ReceivedLength = -1;
            public long ReceivedTime = -1;
            public void HandlePauseEvent(long pauseLength, long pauseEndTime)
            {
                ReceivedLength = pauseLength;
                ReceivedTime = pauseEndTime;
            }
        }

        [Fact]
        public void TestPauseEventIsHandledCorrectly()
        {
            var listener = new TestListener();
            listener.HandlePauseEvent(555L, 999L);

            Assert.Equal(555L, listener.ReceivedLength);
            Assert.Equal(999L, listener.ReceivedTime);
        }
    }
}
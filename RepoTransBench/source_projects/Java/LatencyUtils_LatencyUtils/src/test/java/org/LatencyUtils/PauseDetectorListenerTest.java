package org.LatencyUtils;

import org.junit.Test;

public class PauseDetectorListenerTest {

    private static class TestListener implements PauseDetectorListener {
        long receivedLength = -1;
        long receivedTime = -1;
        @Override
        public void handlePauseEvent(long pauseLength, long pauseEndTime) {
            receivedLength = pauseLength;
            receivedTime = pauseEndTime;
        }
    }

    @Test
    public void testPauseEventIsHandledCorrectly() {
        TestListener listener = new TestListener();
        listener.handlePauseEvent(555L, 999L);

        assert listener.receivedLength == 555L;
        assert listener.receivedTime == 999L;
    }
}
package org.LatencyUtils;

import org.junit.Assert;
import org.junit.Test;

/**
 * Public test for {@link org.LatencyUtils.PauseDetectorListener}
 * Different value and custom listener
 */
public class PauseDetectorListenerPublicTest {
    @Test
    public void testListenerIsCalledWithDifferentArgs() {
        final boolean[] wasCalled = {false};
        PauseDetector.Listener listener = new PauseDetector.Listener() {
            @Override
            public void handlePauseEvent(long pauseLength, long pauseEndTime) {
                wasCalled[0] = (pauseLength == 777L && pauseEndTime == 5555L);
            }
        };
        PauseDetector.Listener[] listeners = new PauseDetector.Listener[]{listener};
        for (PauseDetector.Listener l : listeners) {
            l.handlePauseEvent(777L, 5555L);
        }
        Assert.assertTrue(wasCalled[0]);
    }
}
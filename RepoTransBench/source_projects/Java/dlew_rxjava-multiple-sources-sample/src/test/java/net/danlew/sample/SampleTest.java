package net.danlew.sample;

import org.junit.Test;

public class SampleTest {

    @Test
    public void testSleep_noInterrupt() {
        // Should complete without exception
        Sample.sleep(10);
    }

    @Test
    public void testSleep_withInterrupt() {
        Thread t = new Thread(() -> {
            Sample.sleep(1000L);
        });
        t.start();
        t.interrupt();
        try {
            t.join(200);
        } catch (InterruptedException e) {
            // ignore
        }
        // No assertion, but method should handle interruption
    }
}
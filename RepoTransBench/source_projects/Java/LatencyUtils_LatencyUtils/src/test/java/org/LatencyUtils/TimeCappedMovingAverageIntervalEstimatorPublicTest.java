package org.LatencyUtils;

import org.junit.Assert;
import org.junit.Test;

import java.util.concurrent.TimeUnit;

/**
 * Public JUnit test for {@link org.LatencyUtils.TimeCappedMovingAverageIntervalEstimator}
 * Uses different intervals and pause times than original.
 */
public class TimeCappedMovingAverageIntervalEstimatorPublicTest {

    static {
        System.setProperty("LatencyUtils.useActualTime", "false");
    }

    @Test
    public void testWindowBehaviorPublic() throws Exception {
        MyArtificialPauseDetectorPublic pauseDetector = new MyArtificialPauseDetectorPublic();
        TimeCappedMovingAverageIntervalEstimator estimator =
                new TimeCappedMovingAverageIntervalEstimator(16, 500_000_000L /* 0.5 sec */, pauseDetector);

        TimeUnit.NANOSECONDS.sleep(10_000_000L);

        long now = 0;

        for (int i = 0; i < 5000; i++) {
            now += 15;
            estimator.recordInterval(now);
        }

        Assert.assertEquals("expected interval to be 15", 15, estimator.getEstimatedInterval(now));

        for (int i = 0; i < 8; i++) {
            now += 30;
            estimator.recordInterval(now);
        }

        Assert.assertEquals("expected interval to be 22", 22, estimator.getEstimatedInterval(now));

        for (int i = 0; i < 4; i++) {
            now += 60;
            estimator.recordInterval(now);
        }

        Assert.assertEquals("expected interval to be 32", 32, estimator.getEstimatedInterval(now));

        pauseDetector.recordPause(600_000_000L, now + 600_000_000L); // shorter pause
        now += 600_000_000L;
        TimeUnit.NANOSECONDS.sleep(10_000_000L);

        Assert.assertEquals("expected interval to be 32", 32, estimator.getEstimatedInterval(now));

        for (int i = 0; i < 4; i++) {
            estimator.recordInterval(now);
            now += 60;
        }
        Assert.assertEquals("expected interval to be 47", 47, estimator.getEstimatedInterval(now));

        now = 1_600_000_000L;
        Assert.assertEquals("expected interval to be MAX_VALUE", Long.MAX_VALUE, estimator.getEstimatedInterval(now));

        estimator.recordInterval(now);

        for (int i = 0; i < 8; i++) {
            now += 10;
            estimator.recordInterval(now);
        }

        Assert.assertEquals("expected interval to be 10", 10, estimator.getEstimatedInterval(now));

        pauseDetector.recordPause(700_000_000L, 2_001_000_000L);
        now = 2_001_000_000L;
        TimeUnit.NANOSECONDS.sleep(10_000_000L);

        estimator.recordInterval(now);

        for (int i = 0; i < 8; i++) {
            now += 15;
            estimator.recordInterval(now);
        }

        now = 2_001_000_000L + (10 * 1_000_000);

        Assert.assertEquals("expected interval to be 1_000_000", 1_000_000, estimator.getEstimatedInterval(now));

        now = 2_700_000_000L;

        // EXTREME: empty window
        Assert.assertEquals("expected interval to be MAX_VALUE", Long.MAX_VALUE, estimator.getEstimatedInterval(now));
    }

    class MyArtificialPauseDetectorPublic extends PauseDetector {
        public volatile long latestPauseEndTime = 0;
        public void recordPause(long length, long when) {
            notifyListeners(length, when);
            latestPauseEndTime = when;
        }
    }
}
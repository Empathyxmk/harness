package org.LatencyUtils;

import org.junit.Assert;
import org.junit.Test;

/**
 * Public JUnit test for {@link org.LatencyUtils.MovingAverageIntervalEstimator}
 * Uses different interval values than the private test.
 */
public class MovingAverageIntervalEstimatorPublicTest {

    static {
        System.setProperty("LatencyUtils.useActualTime", "false");
    }

    @Test
    public void testMovingAverageIntervalEstimatorPublic() throws Exception {
        MovingAverageIntervalEstimator estimator = new MovingAverageIntervalEstimator(512);

        long now = 0;

        // Different intervals: start with 25
        for (int i = 0; i < 8000; i++) {
            now += 25;
            estimator.recordInterval(now);
        }

        Assert.assertEquals("expected interval to be 25", 25, estimator.getEstimatedInterval(now));

        // Next, add 400 samples of interval = 50
        for (int i = 0; i < 400; i++) {
            now += 50;
            estimator.recordInterval(now);
        }

        Assert.assertEquals("expected interval to be 37", 37, estimator.getEstimatedInterval(0));

        // Next, add 200 samples of interval = 80
        for (int i = 0; i < 200; i++) {
            now += 80;
            estimator.recordInterval(now);
        }

        Assert.assertEquals("expected interval to be 53", 53, estimator.getEstimatedInterval(0));
    }
}
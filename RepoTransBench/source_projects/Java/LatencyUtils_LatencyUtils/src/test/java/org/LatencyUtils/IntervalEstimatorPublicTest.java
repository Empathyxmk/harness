package org.LatencyUtils;

import org.junit.Test;

/**
 * Public JUnit test for {@link org.LatencyUtils.IntervalEstimator}
 * Uses a different return value.
 */
public class IntervalEstimatorPublicTest {

    @Test
    public void testAbstractMethodReturnsDifferentValue() {
        IntervalEstimator estimator = new IntervalEstimator() {
            @Override
            public void recordInterval(long when) {}

            @Override
            public long getEstimatedInterval(long when) { return 456L; }
        };
        estimator.recordInterval(100L);
        long est = estimator.getEstimatedInterval(101L);
        assert est == 456L;
    }
}
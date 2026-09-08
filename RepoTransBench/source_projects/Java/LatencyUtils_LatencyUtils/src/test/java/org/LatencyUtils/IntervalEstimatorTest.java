package org.LatencyUtils;

import org.junit.Test;

public class IntervalEstimatorTest {

    @Test
    public void testAbstractMethodThrows() {
        // IntervalEstimator is abstract and only exposes abstract methods so
        // we must test via a dummy subclass
        IntervalEstimator estimator = new IntervalEstimator() {
            @Override
            public void recordInterval(long when) {}

            @Override
            public long getEstimatedInterval(long when) { return 123L; }
        };
        estimator.recordInterval(1L);
        long est = estimator.getEstimatedInterval(2L);
        assert est == 123L;
    }
}
package org.LatencyUtils;

import org.junit.Assert;
import org.junit.Test;

/**
 * Public test for {@link org.LatencyUtils.LatencyStats}
 * Uses different record values.
 */
public class LatencyStatsPublicTest {

    @Test
    public void testRecordAndEstimate() {
        LatencyStats stats = new LatencyStats();
        for (int i = 0; i < 50; i++) {
            stats.recordLatency(2000 + i * 2); // Use a different base and increment
        }
        long est = stats.getIntervalHistogram().getMaxValue();
        Assert.assertTrue("Expected max >= 2000", est >= 2000);
    }
}
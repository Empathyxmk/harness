package org.LatencyUtils;

import org.junit.Assert;
import org.junit.Test;

/**
 * Public test for {@link org.LatencyUtils.TimeServices}
 * Uses different increment value.
 */
public class TimeServicesPublicTest {

    @Test
    public void testNanoTimeAndForward() {
        long start = TimeServices.nanoTime();
        TimeServices.moveTimeForwardMsec(16); // Different step from original test (which uses 1 and 1000)
        long end = TimeServices.nanoTime();
        Assert.assertEquals(start + 16_000_000, end);
    }
}
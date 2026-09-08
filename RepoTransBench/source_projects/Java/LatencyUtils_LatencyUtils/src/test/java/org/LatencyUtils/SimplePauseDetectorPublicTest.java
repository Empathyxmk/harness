package org.LatencyUtils;

import org.junit.Assert;
import org.junit.Test;

/**
 * Public test for {@link org.LatencyUtils.SimplePauseDetector}
 * Different configuration from original.
 */
public class SimplePauseDetectorPublicTest {

    @Test
    public void testGetResolution() {
        SimplePauseDetector detector = new SimplePauseDetector(10, 4);
        Assert.assertEquals(10, detector.getResolutionMillis());
    }

    @Test
    public void testSetVerbose() {
        SimplePauseDetector detector = new SimplePauseDetector(3, 2);
        detector.setVerbose(true);
        Assert.assertTrue(detector.isVerbose());
        detector.setVerbose(false);
        Assert.assertFalse(detector.isVerbose());
    }
}
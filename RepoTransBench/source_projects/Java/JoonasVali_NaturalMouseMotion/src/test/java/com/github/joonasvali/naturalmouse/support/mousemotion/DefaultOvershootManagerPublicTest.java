package com.github.joonasvali.naturalmouse.support.mousemotion;

import com.github.joonasvali.naturalmouse.support.DefaultOvershootManager;
import org.junit.Test;

import java.util.Random;

import static org.junit.Assert.assertEquals;

public class DefaultOvershootManagerPublicTest {

    @Test
    public void testNoOvershootsWhenMaxIsZero() {
        DefaultOvershootManager m = new DefaultOvershootManager(new Random(123), 0, 10, 5, 0, true);
        int overshoots = m.getOvershoots(200);
        assertEquals(0, overshoots);
    }

    @Test
    public void testGetOvershootsNonzero() {
        DefaultOvershootManager m = new DefaultOvershootManager(new Random(456), 3, 9, 5, 0.5, false);
        int val = m.getOvershoots(600);
        // Our test data -- different RNG and values than private, but still valid
        // For maxOvershoots=3, minDistanceForOvershoots=9, firstOvershootThreshold=5
        // Check that we get a result in 0..3
        boolean resultInValidRange = (val >= 0 && val <= 3);
        assertEquals(true, resultInValidRange);
    }
}
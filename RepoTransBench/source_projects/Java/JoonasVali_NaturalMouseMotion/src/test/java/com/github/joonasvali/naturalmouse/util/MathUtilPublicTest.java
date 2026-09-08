package com.github.joonasvali.naturalmouse.util;

import org.junit.Test;
import static org.junit.Assert.*;

public class MathUtilPublicTest {

    @Test
    public void testCapIncreasesSmall() {
        // Use different input than private
        assertEquals(7.0, MathUtil.cap(7.0, 2.0, 20.0), 1e-8);
    }

    @Test
    public void testCapCapsHigh() {
        assertEquals(25.0, MathUtil.cap(30.0, 5.0, 25.0), 1e-8);
    }

    @Test
    public void testCapCapsLow() {
        assertEquals(3.5, MathUtil.cap(1.5, 3.5, 10.0), 1e-8);
    }

    @Test
    public void testAverageWide() {
        assertEquals(5.0, MathUtil.average(2.0, 8.0), 1e-8);
    }

    @Test
    public void testAverageNegative() {
        assertEquals(-2.5, MathUtil.average(-5.0, 0.0), 1e-8);
    }
}
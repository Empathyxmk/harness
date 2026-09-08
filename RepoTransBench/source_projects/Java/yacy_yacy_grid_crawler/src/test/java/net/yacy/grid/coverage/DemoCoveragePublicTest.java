package net.yacy.grid.coverage;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DemoCoveragePublicTest {

    @Test
    public void testAddOne_Public() {
        // Use different value than original test (original might use e.g. 5 -> 6), let's use 42 -> 43
        int result = DemoCoverage.addOne(42);
        assertEquals(43, result);
    }

    @Test
    public void testSubtractOne_Public() {
        // Use different value than original (if 5 was used, try 12)
        int result = DemoCoverage.subtractOne(12);
        assertEquals(11, result);
    }

    @Test
    public void testAddOneWithNegativeValue_Public() {
        // Negative number
        int result = DemoCoverage.addOne(-7);
        assertEquals(-6, result);
    }
}
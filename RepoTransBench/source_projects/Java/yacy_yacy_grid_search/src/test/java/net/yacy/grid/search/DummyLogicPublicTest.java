package net.yacy.grid.search;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DummyLogicPublicTest {
    @Test
    void testAddDifferentNumbers() {
        DummyLogic d = new DummyLogic();
        assertEquals(15, d.add(8, 7));
        assertEquals(-5, d.add(-2, -3));
        assertEquals(5, d.add(15, -10));
        assertEquals(0, d.add(10, -10));
        assertEquals(0, d.add(-8, 8));
        assertEquals(14, d.add(10, 4));
    }

    @Test
    void testIsPositiveDifferent() {
        DummyLogic d = new DummyLogic();
        assertTrue(d.isPositive(1));
        assertFalse(d.isPositive(-1));
        assertFalse(d.isPositive(0));
    }

    @Test
    void testDescribeDifferentData() {
        DummyLogic d = new DummyLogic();
        assertEquals("equal", d.describe(-3, -3));
        assertEquals("greater", d.describe(12, 5));
        assertEquals("less", d.describe(-10, 0));
    }
}
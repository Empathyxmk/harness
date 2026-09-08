package net.yacy.grid.search;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DummyLogicTest {
    @Test
    void testAdd() {
        DummyLogic d = new DummyLogic();
        assertEquals(7, d.add(3, 4));
        assertEquals(-7, d.add(-3, -4));
        assertEquals(0, d.add(-3, 3));
        assertEquals(0, d.add(0, 0));
        assertEquals(0, d.add(-3, 3));
        assertEquals(0, d.add(3, -3));
    }

    @Test
    void testIsPositive() {
        DummyLogic d = new DummyLogic();
        assertTrue(d.isPositive(10));
        assertFalse(d.isPositive(0));
        assertFalse(d.isPositive(-4));
    }

    @Test
    void testDescribe() {
        DummyLogic d = new DummyLogic();
        assertEquals("equal", d.describe(5, 5));
        assertEquals("greater", d.describe(7, 2));
        assertEquals("less", d.describe(3, 7));
    }
}
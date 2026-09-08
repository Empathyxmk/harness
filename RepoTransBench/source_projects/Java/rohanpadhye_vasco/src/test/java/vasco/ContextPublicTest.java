package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class ContextPublicTest {
    @Test
    public void testContextEqualsDifferent() {
        Context c1 = new Context("X", 9);
        Context c2 = new Context("X", 9);
        Context c3 = new Context("Y", 20);

        assertEquals(c1, c2);
        assertNotEquals(c1, c3);
    }

    @Test
    public void testContextHashCodeDifferent() {
        Context c1 = new Context("X", 9);
        Context c2 = new Context("X", 9);
        assertEquals(c1.hashCode(), c2.hashCode());
    }

    @Test
    public void testNullContextDifferent() {
        Context c1 = new Context(null, 42);
        Context c2 = new Context(null, 42);
        assertEquals(c1, c2);
    }

    @Test
    public void testContextToStringDifferent() {
        Context c1 = new Context("DifferentMethod", 99);
        assertTrue(c1.toString().contains("DifferentMethod"));
    }
}
package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class ContextTest {
    @Test
    public void testContextEquals() {
        Context c1 = new Context("A", 1);
        Context c2 = new Context("A", 1);
        Context c3 = new Context("B", 2);

        assertEquals(c1, c2);
        assertNotEquals(c1, c3);
    }

    @Test
    public void testContextHashCode() {
        Context c1 = new Context("A", 1);
        Context c2 = new Context("A", 1);
        assertEquals(c1.hashCode(), c2.hashCode());
    }

    @Test
    public void testNullContext() {
        Context c1 = new Context(null, 0);
        Context c2 = new Context(null, 0);
        assertEquals(c1, c2);
    }

    @Test
    public void testContextToString() {
        Context c1 = new Context("Method", 5);
        assertTrue(c1.toString().contains("Method"));
    }
}
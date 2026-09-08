package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class CallSiteTestExtra {
    @Test
    public void testEqualsAndHashCode() {
        CallSite cs1 = new CallSite("foo", 1);
        CallSite cs2 = new CallSite("foo", 1);
        CallSite cs3 = new CallSite("bar", 2);

        assertEquals(cs1, cs2);
        assertNotEquals(cs1, cs3);
        assertEquals(cs1.hashCode(), cs2.hashCode());
        assertNotEquals(cs1.hashCode(), cs3.hashCode());
    }

    @Test
    public void testToString() {
        CallSite cs = new CallSite("main", 3);
        String str = cs.toString();
        assertTrue(str.contains("main"));
        assertTrue(str.contains("3"));
    }
}
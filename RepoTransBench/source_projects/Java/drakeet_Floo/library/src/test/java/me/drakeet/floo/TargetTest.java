package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class TargetTest {

    @Test
    public void testTargetConstructorsAndEquals() {
        Target t1 = new Target("route", "activity");
        Target t2 = new Target("route", "activity");
        Target t3 = new Target("route2", "activity");
        assertEquals("route", t1.route);
        assertEquals("activity", t1.targetClass);
        assertEquals(t1, t2);
        assertNotEquals(t1, t3);
        assertNotEquals(t1, null);
        assertNotEquals(t1, new Object());
        assertEquals(t1.hashCode(), t2.hashCode());
    }
}
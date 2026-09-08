package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class TargetMapTest {

    @Test
    public void testPutAndGet() {
        TargetMap map = new TargetMap();
        Target t1 = new Target("route1", "activity1");
        map.put("key", t1);

        assertTrue(map.containsKey("key"));
        assertEquals(t1, map.get("key"));
    }

    @Test
    public void testRemove() {
        TargetMap map = new TargetMap();
        Target t1 = new Target("route2", "activity2");
        map.put("rm", t1);
        map.remove("rm");
        assertFalse(map.containsKey("rm"));
    }

    @Test
    public void testIsEmpty() {
        TargetMap map = new TargetMap();
        assertTrue(map.isEmpty());
        map.put("a", new Target("a", "a"));
        map.remove("a");
        assertTrue(map.isEmpty());
    }
}
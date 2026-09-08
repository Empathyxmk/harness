package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class ContextTransitionTableTestExtra {
    @Test
    public void testPutAndGetContextTransition() {
        ContextTransitionTable<Integer, String> table = new ContextTransitionTable<>();
        table.put("foo", 1, 2);
        table.put("foo", 1, 3);
        assertTrue(table.get("foo", 1).contains(2));
        assertTrue(table.get("foo", 1).contains(3));
    }

    @Test
    public void testEmpty() {
        ContextTransitionTable<Integer, String> table = new ContextTransitionTable<>();
        assertTrue(table.get("bar", 42).isEmpty());
    }
}
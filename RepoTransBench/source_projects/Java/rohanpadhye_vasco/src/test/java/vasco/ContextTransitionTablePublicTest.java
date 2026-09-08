package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class ContextTransitionTablePublicTest {

    @Test
    public void testDifferentTransitionTable() {
        ContextTransitionTable<String, Integer, Double> table = new ContextTransitionTable<>();
        Context<String, Integer, Double> base = new Context<>("foo", 123);
        Context<String, Integer, Double> next = new Context<>("bar", 321);
        table.put(base, "edge", next);

        assertTrue(table.containsTransition(base, "edge"));
        assertFalse(table.containsTransition(base, "nonexistent"));
        assertEquals(next, table.getTarget(base, "edge"));
        assertNull(table.getTarget(base, "noTransition"));
    }

    @Test
    public void testNullBaseContextTable() {
        ContextTransitionTable<String, Integer, Double> table = new ContextTransitionTable<>();
        Context<String, Integer, Double> base = new Context<>(null, -1);
        Context<String, Integer, Double> next = new Context<>("baz", 888);
        table.put(base, "x", next);

        assertTrue(table.containsTransition(base, "x"));
        assertEquals(next, table.getTarget(base, "x"));
    }

}
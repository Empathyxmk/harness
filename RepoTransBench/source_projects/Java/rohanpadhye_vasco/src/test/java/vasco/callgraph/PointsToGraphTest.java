package vasco.callgraph;

import org.junit.Test;
import static org.junit.Assert.*;

public class PointsToGraphTest {
    @Test
    public void testBasicUsage() {
        PointsToGraph<String, String> ptg = new PointsToGraph<>();
        ptg.add("a", "x");
        ptg.add("a", "y");
        ptg.add("b", "z");

        assertTrue(ptg.get("a").contains("x"));
        assertTrue(ptg.get("a").contains("y"));
        assertTrue(ptg.get("b").contains("z"));
        assertFalse(ptg.get("a").contains("z"));
    }

    @Test
    public void testMerge() {
        PointsToGraph<String, String> g1 = new PointsToGraph<>();
        PointsToGraph<String, String> g2 = new PointsToGraph<>();
        g1.add("A", "one");
        g2.add("A", "two");
        g1.merge(g2);
        assertTrue(g1.get("A").contains("one"));
        assertTrue(g1.get("A").contains("two"));
    }
}
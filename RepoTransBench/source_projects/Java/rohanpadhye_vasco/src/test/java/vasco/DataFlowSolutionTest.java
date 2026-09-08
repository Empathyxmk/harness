package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.*;

public class DataFlowSolutionTest {
    @Test
    public void testSetAndGet() {
        DataFlowSolution<String, Integer> dfs = new DataFlowSolution<>();
        dfs.set("A", Collections.singleton(42));
        assertTrue(dfs.get("A").contains(42));
        assertTrue(dfs.keySet().contains("A"));
    }

    @Test
    public void testMerge() {
        DataFlowSolution<String, Integer> dfs1 = new DataFlowSolution<>();
        DataFlowSolution<String, Integer> dfs2 = new DataFlowSolution<>();
        dfs1.set("A", Collections.singleton(1));
        dfs2.set("A", Collections.singleton(2));
        dfs1.merge(dfs2);
        assertTrue(dfs1.get("A").contains(1));
        assertTrue(dfs1.get("A").contains(2));
    }

    @Test
    public void testToString() {
        DataFlowSolution<String, Integer> dfs = new DataFlowSolution<>();
        dfs.set("B", Collections.singleton(100));
        String str = dfs.toString();
        assertTrue(str.contains("B"));
    }
}
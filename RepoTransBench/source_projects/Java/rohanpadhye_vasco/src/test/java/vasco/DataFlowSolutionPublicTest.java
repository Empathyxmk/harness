package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.*;

public class DataFlowSolutionPublicTest {

    @Test
    public void testDifferentInOutValues() {
        Map<String, Integer> in = new HashMap<>();
        in.put("A", 111);
        in.put("B", 222);
        Map<String, Integer> out = new HashMap<>();
        out.put("A", 777);
        out.put("B", 888);
        DataFlowSolution<String, Integer> dfs = new DataFlowSolution<>(in, out);

        assertEquals(Integer.valueOf(111), dfs.getValueBefore("A"));
        assertEquals(Integer.valueOf(222), dfs.getValueBefore("B"));
        assertEquals(Integer.valueOf(777), dfs.getValueAfter("A"));
        assertEquals(Integer.valueOf(888), dfs.getValueAfter("B"));
    }

    @Test
    public void testNullReturnFromMaps() {
        Map<String, Integer> in = new HashMap<>();
        Map<String, Integer> out = new HashMap<>();
        DataFlowSolution<String, Integer> dfs = new DataFlowSolution<>(in, out);

        assertNull(dfs.getValueBefore("notPresent"));
        assertNull(dfs.getValueAfter("notPresent"));
    }
}
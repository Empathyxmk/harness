package vasco.callgraph;

import org.junit.Test;
import static org.junit.Assert.*;

public class CallGraphTest {
    @Test
    public void basicCoverage() {
        CallGraph<String> cg = new CallGraph<>();
        cg.addEdge("A", "B");
        cg.addEdge("A", "C");
        cg.addEdge("B", "D");

        assertTrue(cg.getCallees("A").contains("B"));
        assertTrue(cg.getCallees("A").contains("C"));
        assertEquals(2, cg.getCallees("A").size());
        assertTrue(cg.getCallers("B").contains("A"));
        assertFalse(cg.getCallees("C").contains("B"));
    }
}
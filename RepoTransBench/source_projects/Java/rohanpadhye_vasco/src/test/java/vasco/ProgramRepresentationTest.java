package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class ProgramRepresentationTest {
    @Test
    public void basicOverrideTest() {
        ProgramRepresentation pr = new ProgramRepresentation() {
            public Object getStartNode() { return "start"; }
            public Object getExitNode() { return "exit"; }
            public Iterable<?> getPreds(Object n) { return null; }
            public Iterable<?> getSuccs(Object n) { return null; }
            public Iterable<?> getAllNodes() { return null; }
            public Object getOwner(Object n) { return null; }
        };

        assertEquals("start", pr.getStartNode());
        assertEquals("exit", pr.getExitNode());
        // further methods just set to return null; we can check no crash
        assertNull(pr.getPreds("x"));
    }
}
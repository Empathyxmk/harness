package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.*;

public class ProgramRepresentationPublicTest {

    @Test
    public void testProgramRepresentationDifferentNodes() {
        ProgramRepresentation pr = new ProgramRepresentation() {
            public Object getStartNode() { return "publicStart"; }
            public Object getExitNode() { return "publicExit"; }
            public Iterable<?> getPreds(Object n) { return Arrays.asList("predX"); }
            public Iterable<?> getSuccs(Object n) { return Arrays.asList("succY"); }
            public Iterable<?> getAllNodes() { return Arrays.asList("publicStart", "publicExit"); }
            public Object getOwner(Object n) { return "ownerZ"; }
        };

        assertEquals("publicStart", pr.getStartNode());
        assertEquals("publicExit", pr.getExitNode());
        assertEquals("ownerZ", pr.getOwner("publicStart"));
        assertTrue(pr.getPreds("publicExit").iterator().hasNext());
        assertTrue(pr.getSuccs("publicStart").iterator().hasNext());
    }

    @Test
    public void testNullIterables() {
        ProgramRepresentation pr = new ProgramRepresentation() {
            public Object getStartNode() { return "begin"; }
            public Object getExitNode() { return "finish"; }
            public Iterable<?> getPreds(Object n) { return null; }
            public Iterable<?> getSuccs(Object n) { return null; }
            public Iterable<?> getAllNodes() { return null; }
            public Object getOwner(Object n) { return null; }
        };

        assertEquals("begin", pr.getStartNode());
        assertEquals("finish", pr.getExitNode());
        assertNull(pr.getOwner("whatever"));
    }
}
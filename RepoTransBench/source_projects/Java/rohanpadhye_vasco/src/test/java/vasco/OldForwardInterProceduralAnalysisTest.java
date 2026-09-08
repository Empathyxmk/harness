package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.*;

public class OldForwardInterProceduralAnalysisTest {
    @Test
    public void testBasicConstructor() {
        ProgramRepresentation pr = new ProgramRepresentation() {
            public Object getStartNode() { return "start"; }
            public Object getExitNode() { return "exit"; }
            public Iterable<?> getPreds(Object n) { return Collections.emptySet(); }
            public Iterable<?> getSuccs(Object n) { return Collections.emptySet(); }
            public Iterable<?> getAllNodes() { return Collections.singleton("start"); }
            public Object getOwner(Object n) { return "owner"; }
        };

        OldForwardInterProceduralAnalysis<Object, String, Integer> ana =
                new OldForwardInterProceduralAnalysis<Object, String, Integer>(pr, null) {
                    @Override
                    protected Set<Integer> apply(Object node, Set<Integer> input) { return input; }
                };
        assertNotNull(ana);
    }
}
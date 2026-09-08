package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class InterProceduralAnalysisTest {
    @Test
    public void trivialAnalysisTest() {
        ProgramRepresentation pr = new ProgramRepresentation() {
            public Object getStartNode() { return "start"; }
            public Object getExitNode() { return "exit"; }
            public Iterable<?> getPreds(Object n) { return null; }
            public Iterable<?> getSuccs(Object n) { return null; }
            public Iterable<?> getAllNodes() { return null; }
            public Object getOwner(Object n) { return null; }
        };

        InterProceduralAnalysis<Object, String, Integer> analysis =
            new ForwardInterProceduralAnalysis<Object, String, Integer>(pr, null) {
                @Override
                protected Set<Integer> apply(Object node, Set<Integer> input) {
                    return input;
                }
            };
        // Should not throw
        assertNotNull(analysis);
    }
}
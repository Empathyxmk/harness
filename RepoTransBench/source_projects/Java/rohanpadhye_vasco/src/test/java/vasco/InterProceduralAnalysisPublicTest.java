package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

public class InterProceduralAnalysisPublicTest {
    @Test
    public void trivialAnalysisPublicTest() {
        ProgramRepresentation pr = new ProgramRepresentation() {
            public Object getStartNode() { return "begin"; }
            public Object getExitNode() { return "end"; }
            public Iterable<?> getPreds(Object n) { return null; }
            public Iterable<?> getSuccs(Object n) { return null; }
            public Iterable<?> getAllNodes() { return null; }
            public Object getOwner(Object n) { return null; }
        };

        InterProceduralAnalysis<Object, String, Double> analysis =
            new ForwardInterProceduralAnalysis<Object, String, Double>(pr, null) {
                @Override
                protected Set<Double> apply(Object node, Set<Double> input) {
                    return input;
                }
            };
        // Should not throw
        assertNotNull(analysis);
    }
}
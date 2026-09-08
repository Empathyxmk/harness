package vasco;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.*;

public class OldForwardInterProceduralAnalysisPublicTest {
    @Test
    public void testDifferentConstructor() {
        ProgramRepresentation pr = new ProgramRepresentation() {
            public Object getStartNode() { return "alpha"; }
            public Object getExitNode() { return "omega"; }
            public Iterable<?> getPreds(Object n) { return Collections.emptySet(); }
            public Iterable<?> getSuccs(Object n) { return Collections.emptySet(); }
            public Iterable<?> getAllNodes() { return Collections.singleton("alpha"); }
            public Object getOwner(Object n) { return "publicOwner"; }
        };

        OldForwardInterProceduralAnalysis<Object, String, Double> ana =
                new OldForwardInterProceduralAnalysis<Object, String, Double>(pr, null) {
                    @Override
                    protected Set<Double> apply(Object node, Set<Double> input) { return input; }
                };
        assertNotNull(ana);
    }
}
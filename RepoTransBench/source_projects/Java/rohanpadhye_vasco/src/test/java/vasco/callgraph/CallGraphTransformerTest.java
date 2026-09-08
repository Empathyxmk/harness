package vasco.callgraph;

import org.junit.Test;
import static org.junit.Assert.*;

public class CallGraphTransformerTest {
    @Test
    public void coverage() {
        CallGraph<String> cg = new CallGraph<>();
        cg.addEdge("A", "B");
        CallGraphTransformer<String> t = new CallGraphTransformer<String>() {
            @Override
            public void transform(CallGraph<String> graph) {
                graph.addEdge("B", "C");
            }
        };
        t.transform(cg);
        assertTrue(cg.getCallees("B").contains("C"));
    }
}
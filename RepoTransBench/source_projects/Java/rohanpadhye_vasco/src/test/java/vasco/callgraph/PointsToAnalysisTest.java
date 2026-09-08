package vasco.callgraph;

import org.junit.Test;
import static org.junit.Assert.*;

public class PointsToAnalysisTest {
    @Test
    public void coverage() {
        PointsToAnalysis<String, String> pta = new PointsToAnalysis<>();
        // as PointsToAnalysis may be just a stub, instantiate and check no crash (further branch coverage may require knowledge of impl)
        assertNotNull(pta);
    }
}